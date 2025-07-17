from cafe_app import create_app, db
from cafe_app.models import Product

app = create_app()

with app.app_context():
    sample_products = [
        Product(name="Espresso", price=8.0),
        Product(name="Cappuccino", price=10.0),
        Product(name="Latte", price=11.5),
        Product(name="Hot chocolate", price=9.0),
        Product(name="green tea", price=7.5),
        Product(name="Croissant", price=6.0),
        Product(name="chicken sandwich", price=15.0),
        Product(name="orange juice", price=10.0),
        Product(name="Still water", price=5.0),
        Product(name="Mineral water", price=5.5)
    ]

    db.session.add_all(sample_products)
    db.session.commit()
    print(" Products have been successfully added to the database.")
