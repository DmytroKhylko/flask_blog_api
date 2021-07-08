from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object("config.DevelopmentConfig")

db = SQLAlchemy(app)

from models.user_model import *
migrate = Migrate(app, db)

@app.route("/")
def home():
    return jsonify({"message":"Hello"})

if __name__ == "__main__":
    app.run(host='0.0.0.0')