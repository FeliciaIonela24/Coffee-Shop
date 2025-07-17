from cafe_app import create_app, db 
#Imports the create_app() function that configures the Flask application and the db (database) object from the cafe_app package.
from cafe_app.models import User
from werkzeug.security import generate_password_hash #Imports the function that encrypts the password to store it securely in the database.

app = create_app()

with app.app_context():#database interaction outside of a real request
    if not User.query.filter_by(username='admin').first(): #create user admin if it does not exist
        admin = User(username='admin', password=generate_password_hash('admin123'))
        db.session.add(admin)
        db.session.commit()
        print("Admin created.")
    else:
        print("Admin already exists.")
