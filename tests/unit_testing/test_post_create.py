import pytest
import json


def test_post_create(client, user_token, create_new_user):
    """
    GIVEN User jwt token
    WHEN a User create new post
    THEN check if new post is created
    """
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
    assert 'new_post_id' in response.get_json()