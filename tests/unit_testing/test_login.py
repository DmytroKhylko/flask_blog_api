import pytest
import json
import base64

def test_login(client, create_new_user):
    """
    GIVEN User
    WHEN a User login
    THEN check if jwt token is returned
    """
    mimetype = 'application/json'
    email_and_pass = "test.email@test.com:strong_password"
    encoded_cred = base64.b64encode(email_and_pass.encode('utf-8'))
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Basic '+ str(encoded_cred, "utf-8")
    }
    url = '/user/login'
    response = client.get(url, headers=headers)
    assert response.status_code == 200
    assert 'token' in response.get_json()