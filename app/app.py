import os
from flask import Flask
from dotenv import load_dotenv
from database import db, migrate

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY', '')
    
    # Database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', '')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    appDir = os.path.dirname(os.path.abspath(__file__))
    db.init_app(app)
    migrate.init_app(app, db, directory=os.path.join(appDir, 'database', 'migrations'))

    return app