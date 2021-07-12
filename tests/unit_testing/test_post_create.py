import pytest
import json

def test_post_create(client, user_token, create_new_user):
    mimetype = 'application/json'
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
    assert response.get_json()['new_post_id']