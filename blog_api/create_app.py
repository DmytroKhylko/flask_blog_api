from flask import Flask
from flask_migrate import Migrate

def create_app(config_filename="blog_api.config.DevelopmentConfig"):
    # config_filename = "blog_api.config.DevelopmentConfig"
    app = Flask(__name__)
    app.config.from_object(config_filename)

    from blog_api.models.db import db
    from blog_api.models.db import migrate


    from blog_api.api import bp
    app.register_blueprint(bp)
    db.init_app(app)
    migrate.init_app(app, db)

    return app