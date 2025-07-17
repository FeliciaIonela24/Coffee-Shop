# Import Flask utilities for routing, rendering templates, handling requests, and flashing messages
from flask import Blueprint, render_template, request, redirect, url_for, flash

# Import Flask-Login utilities for user authentication
from flask_login import login_user, logout_user, login_required, current_user

# Import the database and models for users, products, and cart items
from .models import db, User, Product, CartItem

# Import password hashing and verification tools
from werkzeug.security import generate_password_hash, check_password_hash

# Import datetime for timestamps
from datetime import datetime

# Create a Blueprint for routing under the 'main' namespace
bp = Blueprint('main', __name__)

# ==================== Helper ====================

# Function to check if the current user is the admin
def is_admin():
    return current_user.is_authenticated and current_user.username == 'admin'

# ==================== Home Route ====================

# Redirect the root URL to the products page
@bp.route('/')
def index():
    return redirect(url_for('main.products'))

# ==================== User Registration ====================

# Route for user registration (sign up)
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get username and password from form
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
            return redirect(url_for('main.register'))
        
        # Create new user with hashed password
        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully.')
        return redirect(url_for('main.login'))
    
    # Render the registration form
    return render_template('register.html')

# ==================== User Login ====================

# Route for user login
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get username and password from form
        username = request.form['username']
        password = request.form['password']
        
        # Look up the user in the database
        user = User.query.filter_by(username=username).first()
        
        # If user exists and password is correct, log in
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.products'))
        
        # Otherwise, show error message
        flash('Login failed.')
    
    # Render the login form
    return render_template('login.html')

# ==================== Logout ====================

# Route to log the user out
@bp.route('/logout')
@login_required
def logout():
    logout_user()  # End user session
    flash('Logged out successfully.')
    return redirect(url_for('main.login'))

# ==================== Products ====================

# Route to display all products
@bp.route('/products')
@login_required
def products():
    products = Product.query.all()  # Fetch all products from database
    return render_template('products.html', products=products)

# ==================== Cart ====================

# Route to add a product to the shopping cart
@bp.route('/add-to-cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    # Create a new cart item for the logged-in user
    item = CartItem(user_id=current_user.id, product_id=product_id)
    db.session.add(item)
    db.session.commit()
    flash('Product added to cart.')
    return redirect(url_for('main.products'))

# Route to view the shopping cart
@bp.route('/cart')
@login_required
def view_cart():
    # Get all cart items for the current user
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price for item in cart_items if item.product)
    return render_template('cart.html', cart_items=cart_items, total=total)

# Route to remove an item from the cart
@bp.route('/remove-from-cart/<int:item_id>', methods=['POST'])
@login_required #module to generate the login message 
def remove_from_cart(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id == current_user.id:
        db.session.delete(item)
        db.session.commit()
        flash('Item removed from cart.')
    return redirect(url_for('main.view_cart'))

# ==================== Receipt ====================

# Route to generate a receipt
@bp.route('/receipt')
@login_required
def receipt():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price for item in cart_items if item.product)
    current_date = datetime.now().strftime("%d.%m.%Y %H:%M")
    return render_template('receipt.html', cart_items=cart_items, total=total, current_date=current_date)

# ==================== Admin - Manage Products ====================

# Admin route to view and add products
@bp.route('/admin/products', methods=['GET', 'POST'])
@login_required
def admin_products():
    if not is_admin():
        flash('Access denied.')
        return redirect(url_for('main.products'))

    if request.method == 'POST':
        name = request.form['name']
        try:
            price = float(request.form['price'])
        except ValueError:
            flash('Invalid price format.')
            return redirect(url_for('main.admin_products'))

        product = Product(name=name, price=price)
        db.session.add(product)
        db.session.commit()
        flash('Product added.')
        return redirect(url_for('main.admin_products'))

    products = Product.query.all()
    return render_template('admin/products.html', products=products)

# Admin route to edit an existing product
@bp.route('/admin/edit-product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    if not is_admin():
        flash('Access denied.')
        return redirect(url_for('main.products'))

    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        product.name = request.form['name']
        try:
            product.price = float(request.form['price'])
        except ValueError:
            flash('Invalid price.')
            return redirect(url_for('main.edit_product', product_id=product.id))

        db.session.commit()
        flash('Product updated.')
        return redirect(url_for('main.admin_products'))

    return render_template('admin/edit_product.html', product=product)

# Admin route to delete a product
@bp.route('/admin/delete-product/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    if not is_admin():
        flash('Access denied.')
        return redirect(url_for('main.products'))

    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted.')
    return redirect(url_for('main.admin_products'))
