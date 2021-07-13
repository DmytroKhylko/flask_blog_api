import os

def normalize_url(db_url):
    if db_url is not None:
        return db_url.replace("postgres://", "postgresql+psycopg2://") 


class Config:
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_ECHO = True

    DB_HOST = os.getenv('DB_HOST')
    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')
    SQLALCHEMY_DATABASE_URI = normalize_url(os.environ.get("DATABASE_URL", f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"))



class TestingConfig(Config):
    TESTING = True

    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')
    TEST_DB_HOST = os.getenv('TEST_DB_HOST')
    TEST_DB_PORT = os.getenv('TEST_DB_PORT')
    TEST_DB_NAME = os.getenv('TEST_DB_NAME')
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"
