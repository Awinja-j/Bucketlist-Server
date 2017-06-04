from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import app, db


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)



if __name__ == '__main__':
    db.create_all()
    manager.run()

# all the database migration commands can be accessed by running the script:
        # $ python manage.py db init
        # $ python manage.py db migrate
        # $ python manage.py db upgrade
        # $ python manage.py db --help

