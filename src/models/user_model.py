from api import db
from sqlalchemy import inspect
import datetime
import uuid
import bcrypt
import jwt

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    public_id = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    name = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    last_login = db.Column(db.DateTime())
    last_request = db.Column(db.DateTime())
    posts = db.relationship('Post', backref='user', lazy=False)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

    @staticmethod
    def log_last_request(decoded_token):
        try:
            User.query.filter_by(public_id=decoded_token['public_id']).update(dict(last_request=datetime.datetime.now()))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return str(e)

    @staticmethod
    def log_last_login(id):
        try:
            User.query.filter_by(id=id).update(dict(last_login=datetime.datetime.now()))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return str(e)

    @staticmethod
    def user_in_db_by_email(email):
        if User.query.filter_by(email=email).first() == None:
            return False
        return True

    @staticmethod
    def create_user(email, name, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        new_user = User(public_id=str(uuid.uuid4()), email=email, name=name, password=hashed_password.decode('utf-8'))
        db.session.add(new_user)
        db.session.commit()
        return {'public_id':new_user.public_id}

    @staticmethod
    def check_user_password(pass_to_check, user_password):
        if bcrypt.checkpw(pass_to_check, user_password):
            return True
        return False

    @staticmethod
    def create_token(user_public_id, secret_key):
        token = jwt.encode({"public_id" : user_public_id, "exp" : datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, secret_key, algorithm="HS256")
        return token