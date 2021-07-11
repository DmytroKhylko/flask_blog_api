class Config:
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = b'\xf8)\n\x05Z6i\n\x93\xcf\xe7\xa3{\xb6\x91 \xa7\xbf\xe1\xce\x12\x9e\xbf\x83'


class DataBase:
    DB_HOST = "db"
    DB_NAME = "postgres"
    DB_USER = "postgres"
    DB_PASS = "1234"
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/postgres"


class DevelopmentConfig(Config, DataBase):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_ECHO = True



class TestingConfig(Config, DataBase):
    TESTING = True
