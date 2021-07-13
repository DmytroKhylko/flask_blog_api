from functools import wraps
import datetime
import jwt
from jwt.exceptions import InvalidSignatureError
from jwt.exceptions import ExpiredSignatureError

from flask import Flask, jsonify, request
from flask import current_app
from flask import Blueprint

from sqlalchemy.exc import IntegrityError

from blog_api.models.db import db
from blog_api.models.user_model import User
from blog_api.models.post_model import Post, Like


bp = Blueprint("index", __name__, url_prefix="/")


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None 

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].lstrip("Bearer").strip()
        
        if not token:
            return jsonify({"error":"Token is missing!"}), 401
        
        try:
            decoded_token = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms="HS256")

        except (InvalidSignatureError, ExpiredSignatureError) as e :
            return jsonify({"error":"Invalid token! "+str(e)}), 401

        User.log_last_request(decoded_token) 

        return f(decoded_token, *args, **kwargs)
    return decorated 


# @app.route("/user/signup", methods=['POST'])
@bp.route("/user/signup", methods=("POST",))
def signup():
    request_data = request.get_json()
    if not request_data['email'] or not request_data['name'] or not request_data['password']:
        return jsonify({"error":"Not enough user info was given!"}), 400
    if User.user_in_db_by_email(request_data['email']):
        return jsonify({"error":f"User with email {request_data['email']} already exists"})

    new_user_pulic_id = User.create_user(request_data['email'], request_data['name'], request_data['password'])
    return jsonify({"new_user_pulic_id":new_user_pulic_id['public_id']}), 201


# @app.route("/user/login")
@bp.route("/user/login", methods=("GET",))
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({"error":"Could not verify"}), 400

    user = User.query.filter_by(email=auth.username).first()
    if not user:
        return jsonify({"error":"Could not verify"}), 400

    try:
        if User.check_user_password(auth.password.encode('utf-8'), user.password.encode('utf-8')):
            token = User.create_token(user.public_id, current_app.config['SECRET_KEY'])
            User.log_last_login(user.id)
            return jsonify({"token":token})
    except ValueError as e:
        return jsonify({"error":str(e)})

    return jsonify({"error":"Could not verify"}), 400


# @app.route("/user/<public_id>/last-activity")
@bp.route("/user/<public_id>/last-activity", methods=("GET",))
def last_login(public_id):
    
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({"error":f"User with public id {public_id} not found!"}), 400
    return jsonify({"last_login":user.last_login,
                    "last_request":user.last_request})


# @app.route("/post/create", methods=['POST'])
@bp.route("/post/create", methods=("POST",))
@token_required
def post_create(decoded_token):
    request_data = request.get_json()
    if not decoded_token['public_id'] or not request_data['title'] or not request_data['text']:
        return jsonify({"error":"Not enough post info was given!"}), 400
    new_post = Post(user_public_id=decoded_token['public_id'], title=request_data['title'], text=request_data['text'], creation_date=datetime.datetime.now())

    db.session.add(new_post)
    db.session.commit()
    return jsonify({"new_post_id":new_post.id}), 201


# @app.route("/post/<int:id>/like", methods=['PUT'])
@bp.route("post/<int:id>/like", methods=("PUT",))
@token_required
def post_like(decoded_token, id):
    new_like = Like(user_public_id=decoded_token['public_id'], post_id=id, date=datetime.datetime.now())
    try:
        db.session.add(new_like)
        db.session.commit()
        return jsonify({"message":"ok"}), 200
    except IntegrityError:
        return jsonify({"error":f"User with public_id {decoded_token['public_id']} already liked post {id}"}), 400


# @app.route("/post/<int:id>/unlike", methods=['PUT'])
@bp.route("/post/<int:id>/unlike", methods=("PUT",))
@token_required
def post_unlike(decoded_token, id):
    unlike = Like.query.filter_by(user_public_id=decoded_token['public_id'], post_id=id).first()
    if not unlike:
        return jsonify({"error":"User didn't like the post"}), 400

    db.session.delete(unlike)
    db.session.commit()
    return jsonify({"message":"ok"})



# @app.route("/post/<int:id>/analytics")
@bp.route("/post/<int:id>/analytics", methods=("GET",))
def post_analytics(id):
    try:
        date_from = datetime.datetime.fromisoformat(request.args['date_from'])
        date_to = datetime.datetime.fromisoformat(request.args['date_to'])
        post = Post.query.filter_by(id=id).first()
        if post == None:
            return jsonify({"error":f"Invalid post id! Post with id {id} doesn't exit!"}), 400
        if post.creation_date > date_to:
            return jsonify({"error":f"Invalid date_to param! Post with id {id} hasn't been created yet"})
        likes = Like.query.filter(Like.id == id, Like.date>=date_from, Like.date<=date_to).count()
        return jsonify({"like_count":likes})
    except KeyError as e:
        return jsonify({"error":str(e)}), 400
    except ValueError as e:
        return jsonify({"error":"Incorrect date format: "+str(e)}), 400
    return jsonify({"date_from":date_from,"date_to":date_to})


# @app.route("/")
@bp.route("/")
def home():
    return jsonify({"message":"ok"})

# if __name__ == "__main__":
#     app.run(host='0.0.0.0')