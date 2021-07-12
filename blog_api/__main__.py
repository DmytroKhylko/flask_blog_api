from flask_migrate import Migrate
from create_app import create_app

app = create_app("config.DevelopmentConfig")
app.run(host='0.0.0.0')
