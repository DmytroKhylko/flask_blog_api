# from api import db
from errors.errors import ErrUserWithEmailAlreadyRegistered
from models import post_model, user_model
from db.db_calls import *

def signup(email, name, password):
    if user_in_db_by_email(email):
        return ErrUserWithEmailAlreadyRegistered(email).toDict()
    return create_user(email, name, password)