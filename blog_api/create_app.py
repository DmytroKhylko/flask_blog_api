from flask import Flask

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    from blog_api.models.db import db
    from blog_api.models.db import migrate

    db.init_app(app)
    migrate.init_app(app, db)

    from blog_api.api import bp
    app.register_blueprint(bp)

    return app