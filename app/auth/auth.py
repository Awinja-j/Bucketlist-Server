import os
import inspect
import sys
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from flask import g, jsonify, request
from flask_httpauth import HTTPTokenAuth
from flask_login import logout_user
from app.models import User, db
from flask.blueprints import Blueprint

auth = Blueprint('auth', __name__, template_folder='templates')

auths = HTTPTokenAuth(scheme='Token')

@auths.verify_token
def verify_token(token):
    # authenticate by token only
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True

@auth.route('/auth/register', methods=['POST'])
def register():
    """Register a user"""
    email = request.json.get('email')
    password = request.json.get('password')
    if email is None or password is None:
        return jsonify(message='missing arguments!'), 400
    if db.session.query(User).filter_by(email=email).first() is not None:
        return jsonify(message=' This user already exists!'), 400
    user = User(email=email, password=password)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify(message="Successfully registered {0}".format(email)), 201

@auth.route('/auth/login', methods=['POST'])
def login():
    if not request.json:
        return ("No JSON file detected.")

    email = request.json.get('email')
    password = request.json.get('password')

    if email is None or password is None:
        return jsonify(message='missing arguments!'), 400

    user = db.session.query(User).filter_by(email=email).first()
    if not user:
        return jsonify(message="error! {0} is not registered".format(email)), 400
    elif user and not user.check_password(password):
        return jsonify(message="error! Invalid password"), 403
    else:
        token = user.generate_auth_token()
        return jsonify({'Authorization': 'Token ' + token.decode('ascii')}), 200
        # return jsonify(message="login succesfull! \n token : {}".format(token), token=token.decode()), 302

@auth.route("/logout")
@auths.login_required
def logout():
    logout_user()
    return jsonify(message="Logout succesfull")