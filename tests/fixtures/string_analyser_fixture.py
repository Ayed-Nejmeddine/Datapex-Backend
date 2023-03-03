"""Here analyser fixtures."""
import pandas as pd
import pytest

from data.models.basic_models import Document


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
