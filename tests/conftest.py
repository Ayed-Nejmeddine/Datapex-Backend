"""Here we can define the configuration of tests."""
import pytest
from rest_framework.test import APIClient

from tests.fixtures import city_fixture
from tests.fixtures import document_fixture
from tests.fixtures import user_fixture

# city fixture
import_city_fixture = city_fixture.import_city_fixture
# user fixture
get_user_fixture = user_fixture.get_user_fixture
phone_verification_fixture = user_fixture.phone_verification_fixture
verify_email_fixture = user_fixture.verify_email_fixture
create_user_fixture = user_fixture.create_user_fixture
auth_user_fixture = user_fixture.auth_user_fixture
# document fixture
upload_document_fixture = document_fixture.upload_document_fixture


@pytest.fixture
def client():
    """Function to create a client instance."""
    return APIClient()
