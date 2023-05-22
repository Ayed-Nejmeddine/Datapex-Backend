import pandas as pd
import pytest

from data.models.basic_models import Document
from data.services.homgenization import HomogenizationAnalyser



@pytest.fixture(name="_load_homogenization_document_fixture")
def load_homogenization_document_fixture():
    """
    Fixture to upload a document
    """
    document = Document.objects.create(
        name="homogenization_analyser_source", document_path="homogenization_analyser_source.csv"
    )
    return document


@pytest.fixture(name="_read_homogenization_document_fixture")
def read_homogenization_document_fixture(_load_homogenization_document_fixture):
    """
    Fixture to load a document into a dataframe
    """
    document = _load_homogenization_document_fixture
    df = (pd.read_csv("tests\\data\\data_test\\homogenization_analyser_source.csv", sep=";"),)
    data = pd.DataFrame(*df)
    return (data, document)


@pytest.fixture(name="_homogenization_doc_analyser_fixture")
def homogenization_doc_analyser_fixture(_read_homogenization_document_fixture):
    """
    Fixture to create a homogenization Analyser instance
    """
    data, doc = _read_homogenization_document_fixture
    doc = HomogenizationAnalyser(data, doc.id)
    return doc