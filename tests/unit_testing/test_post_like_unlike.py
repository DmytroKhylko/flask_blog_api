import pytest
import json

def test_post_like_unlike(client, user_token, create_new_user, new_post_id):
    """
    GIVEN User, Post
    WHEN a User like or unlike post
    THEN check if user can like unliked post, can't like already liked post, can't unlike unliked post and can unlike liked post
    """
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer '+ user_token
    }

    url = f'/post/{new_post_id}/like'
    response = client.put(url, headers=headers)
    assert response.status_code == 200

    response = client.put(url, headers=headers)
    assert response.status_code == 400

    url = f'/post/{new_post_id}/unlike'
    response = client.put(url, headers=headers)
    assert response.status_code == 200

    response = client.put(url, headers=headers)
    assert response.status_code == 400


