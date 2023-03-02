"""Here all base indicator test fixtures."""
import pandas as pd
import pytest

from data.models.basic_models import Document
from data.services.syntactic.abstracts import BaseAbstract
from data.services.syntactic.date import DateAnalyser
from data.services.syntactic.number import NumberAnalyser


@pytest.fixture(name="_load_document_fixture")
def load_document_fixture():
    """
    Fixture to upload a document
    """
    document = Document.objects.create(
        name="base_abstract_source", document_path="base_abstract_source.csv"
    )
    return document


@pytest.fixture(name="_read_document_fixture")
def read_document_fixture(_load_document_fixture):
    """
    Fixture to load a document into a dataframe
    """
    document = _load_document_fixture
    df = (pd.read_csv("tests\\data\\data_test\\base_abstract_source.csv", sep=";"),)
    data = pd.DataFrame(*df)
    return (data, document)


@pytest.fixture(name="_number_indicator_fixture")
def number_indicator_fixture(_read_document_fixture):
    """
    Fixture to create a NumberAnalyser instance
    """
    data, doc = _read_document_fixture
    number_indicator = NumberAnalyser(data, doc.id)
    return number_indicator


@pytest.fixture(name="_base_indicator_fixture")
def base_indicator_fixture(_read_document_fixture):
    """
    Fixture to create a BaseAbstract instance
    """
    data, doc = _read_document_fixture
    doc = BaseAbstract(data, doc.id)
    return doc


@pytest.fixture(name="_date_indicator_fixture")
def date_indicator_fixture():
    """
    Fixture to create a DateAnalyser instance
    """
    document = Document.objects.create(name="date_test.csv", document_path="date_test.csv")
    df = (pd.read_csv("tests\\data\\data_test\\date_test.csv", sep=";"),)
    dataframe = pd.DataFrame(*df)
    date_analyser = DateAnalyser(dataframe, document.id)
    return document, date_analyser
