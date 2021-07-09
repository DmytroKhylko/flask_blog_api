class Config(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = b'\xf8)\n\x05Z6i\n\x93\xcf\xe7\xa3{\xb6\x91 \xa7\xbf\xe1\xce\x12\x9e\xbf\x83'


class DataBase(object):
    DB_HOST = "db"
    DB_NAME = "postgres"
    DB_USER = "postgres"
    DB_PASS = "1234"
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/postgres"

    

class ProductionConfig(Config, DataBase):
    DEBUG = False


class DevelopmentConfig(Config, DataBase):
    DEVELOPMENT = True
    DEBUG = True

class StagingConfig(Config, DataBase):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config, DataBase):
    TESTING = True
