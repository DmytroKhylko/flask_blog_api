from .db import db
from sqlalchemy import inspect

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer(), primary_key=True)
    user_public_id = db.Column(db.String(), db.ForeignKey("users.public_id"), nullable=False)
    title = db.Column(db.String(), nullable=False)
    text = db.Column(db.Text(), nullable=False)
    creation_date = db.Column(db.DateTime(), nullable=False)
    likes_dislikes = db.relationship('Like', backref='likes_dislikes', lazy=True)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


class Like(db.Model):
    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key=True)
    user_public_id = db.Column(db.String(), db.ForeignKey("users.public_id"), nullable=False)
    post_id = db.Column(db.Integer(), db.ForeignKey("posts.id"), nullable=False)
    date = db.Column(db.DateTime())
    db.UniqueConstraint(user_public_id, post_id)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }