from flask import g, jsonify, request
from app import app
from flask_httpauth import HTTPBasicAuth
from flask_login import login_required, login_user, logout_user
from app.models import db, User

auth = HTTPBasicAuth()


@auth.verify_password
def verify_token(token, password):
    # authenticate by token only
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True


@app.route('/auth/register', methods=['POST'])
def register():
    """Register a user"""
    email = request.json.get('email')
    password = request.json.get('password')
    if email is None or password is None:
        return jsonify(message='missing arguments!'), 400
    if User.query.filter_by(email=email).first() is not None:
        return jsonify(message=' This user already exists!'), 400
    user = User(email=email, password=password)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify(message="Successfully registered {0}".format(email)), 201

@app.route('/login', methods=['POST'])
def login():
    if not request.json:
        return ("No JSON file detected.")

    email = request.json.get('email')
    password = request.json.get('password')

    if email is None or password is None:
        return jsonify(message='missing arguments!'), 400

    user = User.query.filter_by(email=email).first()
    if not User:
        return jsonify(message = "error! {0} is not registered".format(email)), 400
    elif User and not user.check_password(password):
        return jsonify(message="error! Invalid password"), 403
    else:
        token = user.generate_auth_token()
        return jsonify(message="login succesfull! \n token : {}".format(token))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return jsonify(message="Logout succesfull")