"""Here user fixitures."""
import pytest
from allauth.account.models import EmailAddress
from phone_verify.models import SMSVerification

from tests.data.data_test.user_data import USER


@pytest.fixture(name="_create_user_fixture")
def create_user_fixture(client, _import_city_fixture):
    """
    Fixture to register a new user
    """
    response = client.post("/rest-auth/registration/", USER, content_type="application/json")
    return response


@pytest.fixture(name="_auth_user_fixture")
def auth_user_fixture(_create_user_fixture, client):
    """
    Fixture to authenticate user
    """
    login = {"email": "manel@example.com", "password": "test-1235&"}
    client.post("/rest-auth/login/", login, content_type="application/json")
    return client


@pytest.fixture(name="_get_user_fixture")
def get_user_fixture(_create_user_fixture, client):
    """
    Fixture to get user
    """
    response = client.get("/rest-auth/user/")
    data = response.data
    return data


@pytest.fixture(name="_phone_verification_fixture")
def phone_verification_fixture(client, _get_user_fixture):
    """
    Fixture to verify the phone number for an authenticate user
    """
    phone = {"phone_number": _get_user_fixture["profile"]["phone"]}
    response_reg = client.post("/api/v1/phone/register/", phone)
    code = SMSVerification.objects.get(
        phone_number=_get_user_fixture["profile"]["phone"]
    ).security_code
    verif = {
        "phone_number": _get_user_fixture["profile"]["phone"],
        "session_token": response_reg.data["session_token"],
        "security_code": code,
    }
    client.post("/api/v1/phone/verify/", verif)
    return client


@pytest.fixture(name="_verify_email_fixture")
def verify_email_fixture(_get_user_fixture):
    """
    Fixture to change the email_is _verified attribut to True
    """
    email = EmailAddress.objects.get(email=_get_user_fixture["email"])
    email.verified = True
    email.save()
