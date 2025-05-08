# app/__init__.py
from dotenv import load_dotenv
load_dotenv()
import os
from flask import Flask
from .models import db
from .routes import routes_bp
from .oauth import init_oauth, auth_bp
from app.config import Config

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    app.secret_key = os.environ.get("SECRET_KEY", "dev")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///local.db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    init_oauth(app)
    app.register_blueprint(routes_bp)
    app.register_blueprint(auth_bp)

    # Register table creation after app context is ready
    with app.app_context():
        db.create_all()

    return app
