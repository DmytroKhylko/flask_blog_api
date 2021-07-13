from flask import Flask
from flask_migrate import Migrate

def create_app(config_filename="blog_api.config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    if config_filename == "blog_api.config.DevelopmentConfig":
        from flask_swagger_ui import get_swaggerui_blueprint
        SWAGGER_URL = '/swagger'
        API_URL = '/static/swagger.json'
        SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
            SWAGGER_URL,
            API_URL,
            config={
                'app_name': "Flask Blog API"
            }
        )
        app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

    from blog_api.models.db import db
    from blog_api.models.db import migrate


    from blog_api.api import bp
    app.register_blueprint(bp)
    db.init_app(app)
    migrate.init_app(app, db)

    return app