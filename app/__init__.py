# app/__init__.py

from flask_api import FlaskAPI
from flask_migrate import Migrate
from flask import request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth


# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()
auth = HTTPBasicAuth()


def create_app(config_name):
    from app.models import User, Bucketlist, Item
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    # migrate = Migrate(db, app)

    @app.route('/auth/register', methods = ['POST'])
    def register_new_user():
        '''Register a user'''
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        email = request.json.get('email')
        password = request.json.get('password')
        if email is None or password is None:
            abort(400) # missing arguments
        if User.query.filter_by(email = email).first() is not None:
            abort(400) # existing user
        user = User(email = email)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify({ 'email': user.email }), 201, {'Location': url_for('get_user', id = user.ID, _external = True)}

    # @app.route('/auth/login', methods = ['POST'])
    # @auth.login_required
    # def login_user(email, password):
    #     return jsonify({ 'data': 'Hello, %s!' % g.user.email })

    # @auth.verify_password
    # def verify_password(username, password):
    #     '''Logs a user in'''
    #     user = User.query.filter_by(email = email).first()
    #     if not user or not user.verify_password(password):
    #         return False
    #     g.user = user
    #     return True
        
    # @app.route('/bucketlists/', methods = ['POST'])
    # def new_bucketlist():
    #     '''Create a new bucket list'''
    #     pass
    # @app.route('/bucketlists/', methods = ['GET'])
    # def list_bucketlists():
    #     '''List all the created bucket lists'''
    #     pass
    # @app.route('/bucketlists/<id>', methods = ['GET'])
    # def single_bucketlist():
    #     '''Get single bucket list'''
    #     pass
    # @app.route('/bucketlists/<id>', methods = ['PUT'])
    # def update_bucketlist():
    #     '''Update this bucket list'''
    #     pass
    # @app.route('/bucketlists/<id>', methods = ['DELETE'])
    # def delete_single_bucketlist():
    #     '''Delete this single bucket list'''
    #     pass
    # @app.route('/bucketlists/<id>/items/', methods = ['POST'])
    # def add_items_in_single_bucketlist():
    #     '''Create a new item in bucket list'''
    #     pass
    # @app.route('/bucketlists/<id>/items/<item_id>', methods = ['PUT'])
    # def update_single_item():
    #     '''Update a bucket list item'''
    #     pass
    # @app.route('/bucketlists/<id>/items/<item_id>', methods = ['DELETE'])
    # def delete_an_item_from_a_single_bucketlist():
    #     '''Delete an item in a bucket list'''
    #     pass

    return app

