import pytest
import json

def test_signup(client, init_database):
    """
    GIVEN new User
    WHEN a new User signed up
    THEN check if new user was created
    """
    init_database.session.remove()
    init_database.drop_all()
    init_database.create_all()

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

    init_database.session.remove()
    init_database.drop_all()