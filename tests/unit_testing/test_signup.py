import pytest
import json

def test_signup(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
    }
    data = json.dumps({
        "email":"test.email@test.com",
        "name":"test_user",
        "password":"strong_password"
    })
    url = '/user/signup'
    response = client.post(url, data=data, headers=headers)
    assert response.status_code == 201