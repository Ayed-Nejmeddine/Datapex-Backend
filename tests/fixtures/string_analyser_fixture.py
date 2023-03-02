"""contains the creation of a document and data frame"""
import pandas as pd
import pytest

from data.models.basic_models import Document


@pytest.fixture(name="_base_element")
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
