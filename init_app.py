from flask import Flask
from blog_api.models.db import db

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    db.init_app(app)

    return app