import pytest
import datetime
import base64
import json

def test_user_last_activity(client, user_token, create_new_user):
    """
    GIVEN User
    WHEN a User didn't login
    THEN check if last_login and last_request was set to null
    """
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer '+ user_token
    }

    url = f'/user/{create_new_user.public_id}/last-activity'
    response = client.get(url, headers=headers)
    response_data = response.get_json()
    assert response.status_code == 200
    assert "last_login" in response_data
    assert "last_request" in response_data
    assert response_data['last_login'] == None
    assert response_data['last_request'] != None


    """
    GIVEN User
    WHEN a User logged in
    THEN check if last_login was set and last_request not set
    """
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

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer '+ user_token
    }


    url = f'/user/{create_new_user.public_id}/last-activity'
    response = client.get(url, headers=headers)
    response_data = response.get_json()
    assert response.status_code == 200
    assert "last_login" in response_data
    assert "last_request" in response_data
    assert response_data['last_login'] != None
    assert response_data['last_request'] != None


    """
    GIVEN logged in User
    WHEN a User did request to server
    THEN check if last_request was set
    """
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer '+ user_token
    }
    data = json.dumps({
        'title':'Testing post',
        'text':'This is a post for testing'
    })
    url = '/post/create'
    response = client.post(url, headers=headers, data=data)
    assert response.status_code == 201
    assert 'new_post_id' in response.get_json()


    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer '+ user_token
    }
    url = f'/user/{create_new_user.public_id}/last-activity'
    response = client.get(url, headers=headers)
    response_data = response.get_json()
    assert response.status_code == 200
    assert "last_login" in response_data
    assert "last_request" in response_data
    assert response_data['last_login'] != None
    assert response_data['last_request'] != None