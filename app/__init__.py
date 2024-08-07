from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from uuid import UUID

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

load_dotenv()
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth.login'

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(UUID(user_id))

    @app.route('/')
    def home():
        return render_template('index.html')

    from app.blueprints.auth import bp as auth_bp
    from app.blueprints.cars import bp as cars_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(cars_bp, url_prefix='/cars')

    return app