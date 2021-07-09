from api import app
from errors.errors import ErrUserWithEmailAlreadyRegistered
from models import post_model, user_model
from db.db_calls import *
import jwt
import datetime

def signup(email, name, password):
    if user_in_db_by_email(email):
        return ErrUserWithEmailAlreadyRegistered(email).toDict()
    return create_user(email, name, password)



def check_user_password(pass_to_check, user_password):
    if bcrypt.checkpw(pass_to_check.encode('utf-8'), user_password.encode('utf-8')):
        return True
    return False


def create_token(user_public_id):
    token = jwt.encode({
            "public_id" : user_public_id,
            "exp" : datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, app.config['SECRET_KEY'], algorithm="HS256")
    return token