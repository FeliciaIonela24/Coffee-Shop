from cafe_app import create_app, db
from cafe_app.models import Product

app = create_app()

with app.app_context():
    sample_products = [
        Product(name="Espresso", price=8.0),
        Product(name="Cappuccino", price=10.0),
        Product(name="Latte", price=11.5),
        Product(name="Ciocolată caldă", price=9.0),
        Product(name="Ceai verde", price=7.5),
        Product(name="Croissant", price=6.0),
        Product(name="Sandwich cu pui", price=15.0),
        Product(name="Suc de portocale", price=10.0),
        Product(name="Apă plată", price=5.0),
        Product(name="Apă minerală", price=5.5)
    ]

    db.session.add_all(sample_products)
    db.session.commit()
    print("✅ Produsele au fost adăugate cu succes în baza de date.")
