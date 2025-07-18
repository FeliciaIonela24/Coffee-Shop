from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .models import db, User

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'  

    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    # Load user for login manager
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
