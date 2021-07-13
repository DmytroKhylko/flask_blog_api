import pytest
import datetime

def test_post_analytics(client, new_post_id):
    """
    GIVEN Post
    WHEN Post analytics is requested 
    THEN check if Post is created and like count for new post is set to 0
    """
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
    }

    url = f'/post/{new_post_id}/analytics?date_from={datetime.datetime.now().isoformat()}&date_to={datetime.datetime.now().isoformat()}'
    response = client.get(url, headers=headers)
    assert response.status_code == 200
    assert 'like_count' in response.get_json()
    assert response.get_json()['like_count'] == 0

    url = f'/post/{2}/analytics?date_from={datetime.datetime.now().isoformat()}&date_to={datetime.datetime.now().isoformat()}'
    response = client.get(url, headers=headers)
    assert response.status_code == 400