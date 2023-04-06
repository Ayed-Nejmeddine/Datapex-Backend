"""Here analyser fixtures."""
import pandas as pd
import pytest

from data.models.basic_models import Document
from data.services.syntactic.abstracts import BaseAbstract
from data.services.syntactic.date import DateAnalyser
from data.services.syntactic.number import NumberAnalyser


@pytest.fixture(name="_element_fixture")
def element(_auth_user_fixture, **kwargs):
    """Fixture to upload a document and add an analyser by arguments"""

    def _element_factory(**kwargs):
        document_name = kwargs.pop("name", "no name found")
        path = kwargs.pop("path", "no path found")
        document = Document.objects.create(name=document_name, document_path=path)
        df = pd.read_csv("tests/data/data_test_csv/" + str(document.document_path), sep=";")
        syntactic_service = kwargs.pop("service", "no service found")
        return syntactic_service(df, document.id), document

    return _element_factory


@pytest.fixture
def base_element(_auth_user_fixture):
    """creates a document"""

    def _element_factory(**kwargs):
        document_name = kwargs.pop("name", "no name found")
        path = kwargs.pop("path", "no path found")
        data = kwargs.pop("d_f", "no data frame found")
        document = Document.objects.create(name=document_name, document_path=path)
        syntactic_service = kwargs.pop("service", "no service found")
        return syntactic_service(data, document.id)

    return _element_factory


@pytest.fixture
def data_frame():
    """creates a dataframe from a csv file"""
    d_f = pd.read_csv(
        "tests\\data\\data_test_csv\\Days.csv", encoding="latin-1", sep=";", keep_default_na=True
    )
    return d_f


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
    df = (pd.read_csv("tests\\data\\data_test_csv\\Days.csv", sep=";"),)
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
