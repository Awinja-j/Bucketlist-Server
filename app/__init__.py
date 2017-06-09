# This is the file that is invoked to start up a development server.
# It gets a copy of the app from your package and runs it.
# This won’t be used in production, but it will see a lot of mileage in development.
import os
import inspect
import sys
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

# create app
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config.config_environments[config_name])
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app