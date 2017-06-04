# This is the file that is invoked to start up a development server.
# It gets a copy of the app from your package and runs it.
# This won’t be used in production, but it will see a lot of mileage in development.

import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object(config.config_environments['development'])

# create app
def create_app():
    db = SQLAlchemy(app)
    db.init_app(app)
    db.create_all()
