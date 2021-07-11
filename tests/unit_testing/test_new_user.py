import pytest
import uuid
import bcrypt
# from ...models.user_model import User

def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the public_id, email, name, password, last_login and last_request are defined correctly
    """
    assert new_user.public_id == uuid.uuid4
    assert new_user.email == "test.email@test.com"
    assert new_user.name == "test_user"
    assert bcrypt.checkpw("strong_password".encode('utf-8'), new_user.password) == True

