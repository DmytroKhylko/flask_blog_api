import pytest
import jwt
import bcrypt
from flask import current_app
from blog_api.models.user_model import User
from blog_api.models.post_model import Post, Like
from blog_api.models.db import db
from blog_api.create_app import create_app

@pytest.fixture
def input_value():
    input_value = 39
    return input_value


@pytest.fixture()
def app():
    app = create_app('blog_api.config.TestingConfig')
 
    # testing_client = app.test_client()
 
    # ctx = app.app_context()
    # ctx.push()
 
    yield app 
 
    # ctx.pop()


@pytest.fixture
def client(app):
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def init_database():
    # db.create_all()
 
    yield db
 
    # db.drop_all()


@pytest.fixture
def new_user():
    user = User(public_id="3da9ef5b-909d-4c32-aca0-c955503676a6", email="test.email@test.com", name="test_user", password="strong_password")
    return user

@pytest.fixture
def create_new_user(new_user):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(new_user.password.encode('utf-8'), salt)
    user = User(public_id=new_user.public_id, email=new_user.email, name=new_user.name, password=hashed_password.decode('utf-8'))
    db.session.add(user)
    db.session.commit()

@pytest.fixture
def user_token(new_user):
        token = User.create_token(new_user.public_id, current_app.config['SECRET_KEY'])
        return token
