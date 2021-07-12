from flask_migrate import Migrate
from blog_api.create_app import create_app

app = create_app("blog_api.config.DevelopmentConfig")
app.run(host='0.0.0.0')
