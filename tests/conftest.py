import pytest
import jwt
import bcrypt
import datetime
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
    yield app 
 

@pytest.fixture
def client(app):
    with app.app_context():
        yield app.test_client()



@pytest.fixture()
def init_database():
    yield db
 

@pytest.fixture
def new_user():
    user = User(public_id="3da9ef5b-909d-4c32-aca0-c955503676a6", email="test.email@test.com", name="test_user", password="strong_password")
    return user

@pytest.fixture
def create_new_user(new_user, init_database):
    init_database.drop_all()
    init_database.create_all()
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(new_user.password.encode('utf-8'), salt)
    user = User(public_id=new_user.public_id, email=new_user.email, name=new_user.name, password=hashed_password.decode('utf-8'))
    init_database.session.add(user)
    init_database.session.commit()
    return user

@pytest.fixture
def user_token(new_user):
        token = User.create_token(new_user.public_id, current_app.config['SECRET_KEY'])
        return token

@pytest.fixture
def new_post_id(new_user, init_database):
    post = Post(user_public_id=new_user.public_id, title="Test post", text="This is a test post", creation_date=datetime.datetime.now())
    init_database.session.add(post)
    init_database.session.commit()
    return post.id