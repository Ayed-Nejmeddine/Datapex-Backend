"""Here document fixitures."""
import os

from django.conf import settings

import pytest


@pytest.fixture(name="_upload_document_fixture")
def upload_document_fixture(_auth_user_fixture, client):
    """
    Fixture to upload document.
    """
    document_path = os.path.join(settings.BASE_DIR, "tests/data/data_test_csv/Days.csv")
    with open(document_path, "rb") as document:
        payload = {"document_path": document}
        response = client.post("/api/v1/upload-document/", data=payload, format="multipart")
    return response.data
