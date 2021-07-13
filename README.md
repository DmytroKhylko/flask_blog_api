## Flask Blog API

#### All necessary variables are stored in ***.env*** file in project top level directory
##### ***.env*** example
```
PORT=5000
SECRET_KEY = \xf8)\n\x05Z6i\n\x93\xcf\xe7\xa3{\xb6\x91 \xa7\xbf\xe1\xce\x12\x9e\xbf\x83
DB_HOST = db
DB_NAME = postgres
DB_USER = postgres
DB_PASS = 1234
DB_PORT = 5432
TEST_DB_HOST = db-test
TEST_DB_PORT = 5432
TEST_DB_NAME = postgres
```
#### To run API, in project top level directory run:
```
docker-compose up
```

#### To run tests run in ***test/*** directory of API docker container:
```
pytest
```
#### Swagger docs are placed under ***/swagger*** API route if config is set to ***DevelopmentConfig***