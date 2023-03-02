"""Here all user tests."""
import json

import pytest

from tests.data.data_test.user_data import USER


@pytest.mark.django_db
def test_register_user(client, _import_city_fixture):
    """Test a seccess of user register."""
    response = client.post("/rest-auth/registration/", USER, content_type="application/json")
    assert response.status_code == 201
    assert "key" in response.data


@pytest.mark.django_db
def test_login_user_success(client, _create_user_fixture):
    """Test a seccess of user login."""
    data_login = json.dumps({"email": "chiraz11@example.com", "password": "test-1235&"})
    response = client.post("/rest-auth/login/", data_login, content_type="application/json")
    assert response.status_code == 200
    assert "key" in response.data


@pytest.mark.django_db
def test_login_user_fail(client, _create_user_fixture):
    """Test a fail of user register."""
    login = {"email": "test@example.com", "password": "test-1235&"}
    response = client.post("/rest-auth/login/", login, content_type="application/json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_logout(_auth_user_fixture):
    """Test a seccess of user logout."""
    response = _auth_user_fixture.post("/rest-auth/logout/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_user_fail(client, _create_user_fixture):
    """Test a fail of get user."""
    response = client.get("/rest-auth/user/")
    data = response.data
    assert data["profile"]["email_is_verified"] is False
    assert data["profile"]["phone_is_verified"] is False


@pytest.mark.django_db
def test_get_user_success(client, _verify_email_fixture, _phone_verification_fixture):
    """Test a success of get user."""
    response = client.get("/rest-auth/user/")
    data = response.data
    assert data["profile"]["phone_is_verified"] is True
    assert data["profile"]["email_is_verified"] is True
