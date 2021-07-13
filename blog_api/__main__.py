from flask_migrate import Migrate
from blog_api.create_app import create_app
import os
app = create_app("blog_api.config.DevelopmentConfig")
app.run(host='0.0.0.0', port=os.getenv("PORT", 5000))
