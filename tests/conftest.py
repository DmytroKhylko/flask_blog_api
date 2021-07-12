import pytest
import uuid
import bcrypt
from blog_api.models.user_model import User
from blog_api.models.post_model import Post, Like
from blog_api.models.db import db
from init_app import create_app

@pytest.fixture
def input_value():
    input_value = 39
    return input_value

@pytest.fixture
def new_user():
    salt = bcrypt.gensalt()
    user = User(public_id=uuid.uuid4, email="test.email@test.com", name="test_user", password=bcrypt.hashpw("strong_password".encode('utf-8'), salt))
    return user

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
    return app.test_client()

# @pytest.fixture()
# def init_database():
#     db.create_all()
 
#     # Commit the changes for the users
 
#     yield db
 
#     # db.drop_all()