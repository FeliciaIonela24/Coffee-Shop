from cafe_app import create_app
from cafe_app.models import db, Product

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    p1 = Product(name="Coffee", price=2.5)
    p2 = Product(name="Tea", price=2.0)

    db.session.add_all([p1, p2])
    db.session.commit()

    print("Products have been added to the database.")
