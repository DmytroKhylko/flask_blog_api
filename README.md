## Flask Blog API

#### All necessary variables are stored in ***.env*** file in api top level directory
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
#### To run API, in api top level directory run:
```
docker-compose up
```

#### To run tests run in ***test/*** directory of API docker container:
```
pytest
```
#### Swagger docs are placed under ***/swagger*** API route if config is set to ***DevelopmentConfig***
#### Migrations are automatically performed on each launch 
#### To perform manual migrations in api top level directory run
```
flask db migrate
flask db upgrade
```
### API requests with cURL
#### Signup new user
```
curl -X POST \
  'http://localhost:5000/user/signup' \
  -H 'Content-Type: application/json' \
  -d '{
    "email":"test.email@test.com",
    "name":"test_user",
    "password":"strong_password"
}'
```
#### Login
```
curl -X GET \
  'http://localhost:5000/user/login' \
  -H 'Authorization: Basic <login:password(encoded in base64)>'
```
#### Create a new post
```
curl -X POST \
  'http://localhost:5000/post/create' \
  -H 'Authorization: Bearer <JWT token you've got after login' \
  -H 'Content-Type: application/json' \
  -d '{
    "title":"My first post",
    "text":"This a post about how I (user 1) created my first post.."
}'
```
#### Post like (unlike is the same but instead of like use unlike in route)
```
curl -X PUT \
  'http://localhost:5000/post/<post_id>/like/' \
  -H 'Accept: */*' \
  -H 'User-Agent: Thunder Client (https://www.thunderclient.io)' \
  -H 'Authorization: Bearer <user JWT token>'
  ```
#### Get post like analitycs
```
curl -X GET \
  'http://localhost:5000/post/analytics?date_from=<ISOdate>&date_to=<ISOdate>' 
    -H 'Authorization: Bearer <JWT token you've got after login'
  ```
#### Get user activity info
```
curl -X GET \
  'http://localhost:5000/user/<user_public_id>/last-activity'
  -H 'Authorization: Bearer <JWT token you've got after login' \
```
