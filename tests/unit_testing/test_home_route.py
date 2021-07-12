import pytest
import json
def test_home_route(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer ' + 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiI4OTg4OTA0Ny0zMDQ3LTRkNjktYWRkMS0wYTM2NzY1MjYwYTciLCJleHAiOjE2MjYwNzAyMTV9.LB-Ob0oT4dYwHDxzE7FR7PWW49XuXZRHs6uwM501raE'
    }
    url = 'post/create'
    response = client.get('/')
    print(client)
    assert response.status_code == 200