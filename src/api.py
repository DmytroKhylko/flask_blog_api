from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import datetime
import bcrypt
import jwt
from functools import wraps


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object("config.DevelopmentConfig")

db = SQLAlchemy(app)

from models.user_model import *
from models.post_model import *
# from models import post_model, user_model
migrate = Migrate(app, db)

import sys

from services import auth_service

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None 

        print(request.headers, file=sys.stdout)
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].lstrip("Bearer").strip()
        
        print(token, file=sys.stdout)
        if not token:
            return jsonify({"error":"Token is missing!"}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
            current_user = User.query.filter_by(public_id=data['public_id']).first()
            if not current_user:
                return jsonify({"error":"Invalid public user id!"})
        except Exception:
            return jsonify({"error":"Invalid token!"}), 401
            
        return f(current_user, *args, **kwargs)

    return decorated 

        

@app.route("/")
@token_required
def home(current_user):
    return jsonify({"message":"Hello"})

@app.route("/user/signup", methods=['POST'])
def signup():
    request_data = request.get_json()
    return jsonify(auth_service.signup(request_data['email'], request_data['name'], request_data['password']))

@app.route("/user/login", methods=['GET'])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
    
    user = User.query.filter_by(email=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if bcrypt.checkpw(auth.password.encode('utf-8'), user.password.encode('utf-8')):
        token = jwt.encode({
            "public_id" : user.public_id,
            "exp" : datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({"token":token})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})


if __name__ == "__main__":
    app.run(host='0.0.0.0')