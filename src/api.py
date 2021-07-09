from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
import datetime
import bcrypt
import jwt
from functools import wraps


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config.from_object("config.DevelopmentConfig")

db = SQLAlchemy(app)

from models.user_model import *
from models.post_model import *
# from models import post_model, user_model
migrate = Migrate(app, db)


from services import auth_service
from psycopg2.errors import UniqueViolation

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None 

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].lstrip("Bearer").strip()
        
        if not token:
            return jsonify({"error":"Token is missing!"}), 401
        
        try:
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")

        except Exception as e :
            return jsonify({"error":"Invalid token! "+str(e)}), 401

        User.query.filter_by(public_id=decoded_token['public_id']).update(dict(last_request=datetime.datetime.now()))
        db.session.commit() 
        return f(decoded_token, *args, **kwargs)
    return decorated 


@app.route("/user/signup", methods=['POST'])
def signup():
    request_data = request.get_json()
    return jsonify(auth_service.signup(request_data['email'], request_data['name'], request_data['password'])), 201

@app.route("/user/login")
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({"error":"Could not verify"}), 401

    user = User.query.filter_by(email=auth.username).first()
    if not user:
        return jsonify({"error":"Could not verify"}), 401

    try:
        if bcrypt.checkpw(auth.password.encode('utf-8'), user.password.encode('utf-8')):
            token = auth_service.create_token(user.public_id)
            User.query.filter_by(id=user.id).update(dict(last_login=datetime.datetime.now()))
            db.session.commit()
            return jsonify({"token":token})
    except ValueError as e:
        return jsonify({"error":str(e)})

    return jsonify({"error":"Could not verify"}), 401


@app.route("/user/<public_id>/last-login")
def last_login(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({"error":f"User with public id {public_id} not found!"}), 401
    return jsonify({"last_loign":user.last_login})


@app.route("/user/<public_id>/last-request")
def last_request(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({"error":f"User with public id {public_id} not found!"}), 401
    return jsonify({"last_request":user.last_login})


@app.route("/post/create", methods=['POST'])
@token_required
def post_create(decoded_token):
    request_data = request.get_json()
    new_post = Post(user_public_id=decoded_token['public_id'], title=request_data['title'], text=request_data['text'], creation_date=datetime.datetime.now())
    try:
        db.session.add(new_post)
        db.session.commit()
        return jsonify({"newPostId":new_post.id}), 201
    except Exception as e:
        return jsonify({"error":str(e)})


@app.route("/post/like", methods=['PUT'])
@token_required
def post_like(decoded_token):
    request_data = request.get_json()
    new_like = Like(user_public_id=decoded_token['public_id'], post_id=request_data['post_id'], date=datetime.datetime.now())
    try:
        db.session.add(new_like)
        db.session.commit()
        return jsonify({"message":"ok"}), 201
    except IntegrityError as e:
        assert isinstance(e.orig, UniqueViolation)
        return jsonify({"error":f"User with public_id {decoded_token['public_id']} already liked post {request_data['post_id']}"})
    except Exception as e:
        return jsonify({"error":str(e)})


@app.route("/post/unlike", methods=['DELETE'])
@token_required
def post_unlike(decoded_token):
    request_data = request.get_json()
    unlike = Like.query.filter_by(user_public_id=decoded_token['public_id'], post_id=request_data['post_id']).first()
    if not unlike:
        return jsonify({"error":"User didn't like the post"})
    try:
        db.session.delete(unlike)
        db.session.commit()
        return jsonify({"message":"ok"})
    except Exception as e:
        return jsonify({"error":str(e)})


@app.route("/post/analytics/<id>")
def post_analytics(id):
    try:
        date_from = datetime.datetime.fromisoformat(request.args['date_from'])
        date_to = datetime.datetime.fromisoformat(request.args['date_to'])
        post = Post.query.filter_by(id=id).first()
        if post == None:
            return jsonify({"error":f"Invalid post id! Post with id {id} doesn't exit!"}), 401
        if post.creation_date > date_to:
            return jsonify({"error":f"Invalid date_to param! Post with id {id} hasn't been created yet"})
        likes = Like.query.filter(Like.post_id == id, Like.date>=date_from, Like.date<=date_to).count()
        return jsonify({"like_count":likes})
    except KeyError as e:
        return jsonify({"error":str(e)}), 400
    except ValueError as e:
        return jsonify({"error":"Incorrect date format: "+str(e)}), 400
    return jsonify({"date_from":date_from,"date_to":date_to})


if __name__ == "__main__":
    app.run(host='0.0.0.0')