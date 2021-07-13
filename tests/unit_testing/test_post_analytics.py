import pytest
import datetime

def test_post_analytics(client, user_token,new_post_id):
    """
    GIVEN Post
    WHEN Post analytics is requested 
    THEN check if analytics is given
    """
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer '+ user_token
    }

    url = f'/post/analytics?date_from={datetime.datetime.now().isoformat()}&date_to={datetime.datetime.now().isoformat()}'
    response = client.get(url, headers=headers)
    assert response.status_code == 200