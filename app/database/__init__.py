import os
from wsgi import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', '')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

databaseDir = os.path.dirname(os.path.abspath(__file__))

db = SQLAlchemy(app)
migrate = Migrate(app, db, directory=os.path.join(databaseDir, 'migrations'))