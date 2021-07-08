from api import db
from models import post_model, user_model
import uuid
import bcrypt

def user_in_db_by_email(email):
    if user_model.User.query.filter_by(email=email).first() == None:
        return False
    return True

def create_user(email, name, password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    new_user = user_model.User(public_id=str(uuid.uuid4()), email=email, name=name, password=hashed_password.decode('utf-8'))
    db.session.add(new_user)
    db.session.commit()
    return {'public_id':new_user.public_id}