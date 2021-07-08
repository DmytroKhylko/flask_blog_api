from api import db
from sqlalchemy import inspect

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    user_public_id = db.Column(db.String(), db.ForeignKey("users.public_id"), nullable=False, unique=True)
    title = db.Column(db.String(), nullable=False)
    text = db.Column(db.Text(), nullable=False)
    likes = db.Column(db.Integer())
    dislikes = db.Column(db.Integer())

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }