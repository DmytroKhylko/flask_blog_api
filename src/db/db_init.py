# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker


# DB_HOST = "db"
# DB_NAME = "postgres"
# DB_USER = "postgres"
# DB_PASS = "1234"

# SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/blog"

# engine = create_engine(SQLALCHEMY_DATABASE_URI)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()