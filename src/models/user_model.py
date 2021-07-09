from api import db
from sqlalchemy import inspect

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