"""Here all document tests."""
import os

from django.conf import settings

import pytest


@pytest.mark.django_db
def test_post_upload_document(_auth_user_fixture, client):
    """Test a seccess of upload document."""
    document_path = os.path.join(settings.BASE_DIR, "tests/data/data_test_csv/Days.csv")
    with open(document_path, "rb") as document:
        payload = {"document_path": document}
        response = client.post("/api/v1/upload-document/", data=payload, format="multipart")
    assert response.status_code == 201


@pytest.mark.django_db
def test_get_all_documents(_upload_document_fixture, client):
    """Test a seccess of get all documents."""
    response = client.get("/api/v1/upload-document/")
    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_get_document_by_id(_upload_document_fixture, client):
    """Test a seccess of get document by id."""
    document_id = _upload_document_fixture.get("id")
    response = client.get(
        f"/api/v1/upload-document/{document_id}/", content_type="application/json"
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_put_document(_upload_document_fixture, client):
    """Test a seccess of put document."""
    document_id = _upload_document_fixture.get("id")
    new_document_path = os.path.join(settings.BASE_DIR, "tests/data/data_test_csv/newDays.csv")
    with open(new_document_path, "rb") as document:
        response = client.put(
            f"/api/v1/upload-document/{document_id}/",
            data={"document_path": document},
            format="multipart",
        )
    assert response.status_code == 200
