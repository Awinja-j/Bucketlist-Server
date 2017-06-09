import os
import inspect
import sys
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from run import app
from config import DevelopmentConfig
from app.api.bucketlist_api import bucket
from app.api.bucketlist_item import item

from app.auth.auth import auth


with app.app_context():
    from app.models import User, Bucketlist, Item, db
    db.init_app(app)
    db.create_all()
app.config.from_object(DevelopmentConfig)
app.register_blueprint(auth)
app.register_blueprint(bucket)
app.register_blueprint(item)
app.url_map.strict_slashes = False


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
