"""Here document fixitures."""
import os

from django.conf import settings

import pandas as pd
import pytest

from data.models.basic_models import Document
from data.services.syntactic import BaseAbstract
from data.services.syntactic import NumberAnalyser
from data.services.syntactic import StringAnalyser


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


@pytest.fixture(name="_string_document_fixture")
def string_document_fixture(_auth_user_fixture):
    doc = Document.objects.create(name="sex", document_path="sex.csv")
    df = pd.read_csv("tests/data/data_test_csv/sex.csv", sep=";", encoding="latin-1")
    string_analyser = StringAnalyser(df, doc.id)
    return string_analyser


@pytest.fixture(name="_number_document_fixture")
def number_document_fixture(_auth_user_fixture):
    doc = Document.objects.create(name="test", document_path="test.csv")
    df = pd.read_csv("tests/data/data_test_csv/test.csv", sep=";", encoding="latin-1")
    string_analyser = NumberAnalyser(df, doc.id)
    return string_analyser


@pytest.fixture(name="_abstract_document_fixture")
def abstract_document_fixture(_auth_user_fixture):
    doc = Document.objects.create(name="test", document_path="test.csv")
    df = pd.read_csv("tests/data/data_test_csv/test.csv", sep=";", encoding="latin-1")
    string_analyser = BaseAbstract(df, doc.id)
    return string_analyser
