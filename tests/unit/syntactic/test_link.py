"""Here the test for link between two columns"""
import pytest

from data.models.basic_models import Link
from data.services.syntactic import NumberAnalyser
from data.services.syntactic import StringAnalyser


@pytest.mark.django_db
def test_link_number(_element_fixture):
    """Test link for number columns"""
    service, document = _element_fixture(name="link.csv", path="link.csv", service=NumberAnalyser)
    service.link()
    link_result = Link.objects.filter(document=document)
    assert link_result[0].first_column == "col4"
    assert link_result[0].second_column == "col5"
    assert link_result[0].relationship == "less-then"

    assert link_result[2].first_column == "col5"
    assert link_result[2].second_column == "col6"
    assert link_result[2].relationship == "equals"


@pytest.mark.django_db
def test_link_string(_element_fixture):
    """Test link for string columns"""
    service, document = _element_fixture(name="link.csv", path="link.csv", service=StringAnalyser)
    service.link()
    link_result = Link.objects.filter(document=document)
    assert link_result[0].relationship == "81.4% similarity score"
