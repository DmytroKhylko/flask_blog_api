from functools import wraps
import datetime
import jwt

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

from models.db import db
from models.user_model import User
from models.post_model import Post, Like

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    from models.db import db
    db.init_app(app)

    return app
    
app = create_app("config.DevelopmentConfig")

migrate = Migrate(app, db)



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
        User.log_last_request(decoded_token) 

        return f(decoded_token, *args, **kwargs)
    return decorated 


@app.route("/user/signup", methods=['POST'])
def signup():
    request_data = request.get_json()
    if User.user_in_db_by_email(request_data['email']):
        return jsonify({"error":f"User with email {request_data['email']} already exists"})
    try:
        new_user_pulic_id = User.create_user(request_data['email'], request_data['name'], request_data['password'])
    except Exception as e:
        return jsonify({"error":str(e)})
    return jsonify({"new_user_pulic_id":new_user_pulic_id['public_id']}), 201


@app.route("/user/login")
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({"error":"Could not verify"}), 401

    user = User.query.filter_by(email=auth.username).first()
    if not user:
        return jsonify({"error":"Could not verify"}), 401

    try:
        if User.check_user_password(auth.password.encode('utf-8'), user.password.encode('utf-8')):
            token = User.create_token(user.public_id, app.config['SECRET_KEY'])
            User.log_last_login(user.id)
            return jsonify({"token":token})
    except ValueError as e:
        return jsonify({"error":str(e)})

    return jsonify({"error":"Could not verify"}), 401


@app.route("/user/<public_id>/last-activity")
def last_login(public_id):
    try:
        user = User.query.filter_by(public_id=public_id).first()
    except Exception as e:
        return jsonify({"error":str(e)})
    if not user:
        return jsonify({"error":f"User with public id {public_id} not found!"}), 401
    return jsonify({"last_loign":user.last_login,
                    "last_request":user.last_request})


@app.route("/post/create", methods=['POST'])
@token_required
def post_create(decoded_token):
    request_data = request.get_json()
    new_post = Post(user_public_id=decoded_token['public_id'], title=request_data['title'], text=request_data['text'], creation_date=datetime.datetime.now())
    try:
        db.session.add(new_post)
        db.session.commit()
        return jsonify({"new_post_id":new_post.id}), 201
    except Exception as e:
        return jsonify({"error":str(e)})


@app.route("/post/<int:id>/like", methods=['PUT'])
@token_required
def post_like(decoded_token, id):
    new_like = Like(user_public_id=decoded_token['public_id'], post_id=id, date=datetime.datetime.now())
    try:
        db.session.add(new_like)
        db.session.commit()
        return jsonify({"message":"ok"}), 201
    except IntegrityError as e:
        assert isinstance(e.orig, UniqueViolation)
        return jsonify({"error":f"User with public_id {decoded_token['public_id']} already liked post {id}"})
    except Exception as e:
        return jsonify({"error":str(e)})


@app.route("/post/<int:id>/unlike", methods=['PUT'])
@token_required
def post_unlike(decoded_token, id):
    unlike = Like.query.filter_by(user_public_id=decoded_token['public_id'], post_id=id).first()
    if not unlike:
        return jsonify({"error":"User didn't like the post"})
    try:
        db.session.delete(unlike)
        db.session.commit()
        return jsonify({"message":"ok"})
    except Exception as e:
        return jsonify({"error":str(e)})


@app.route("/post/<int:id>/analytics")
def post_analytics(id):
    try:
        date_from = datetime.datetime.fromisoformat(request.args['date_from'])
        date_to = datetime.datetime.fromisoformat(request.args['date_to'])
        post = Post.query.filter_by(id=id).first()
        if post == None:
            return jsonify({"error":f"Invalid post id! Post with id {id} doesn't exit!"}), 401
        if post.creation_date > date_to:
            return jsonify({"error":f"Invalid date_to param! Post with id {id} hasn't been created yet"})
        likes = Like.query.filter(Like.id == id, Like.date>=date_from, Like.date<=date_to).count()
        return jsonify({"like_count":likes})
    except KeyError as e:
        return jsonify({"error":str(e)}), 400
    except ValueError as e:
        return jsonify({"error":"Incorrect date format: "+str(e)}), 400
    return jsonify({"date_from":date_from,"date_to":date_to})


if __name__ == "__main__":
    app.run(host='0.0.0.0')