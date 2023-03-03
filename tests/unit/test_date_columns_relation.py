""""Here all date tests."""
import pytest

from data.models.basic_models import Link


@pytest.mark.django_db
def test_link_should_success(_date_indicator_fixture):
    """
    Test of the link function in DateAnalyser class
    """
    document, date_analyser = _date_indicator_fixture
    date_analyser.link()
    assert Link.objects.last().relationship == "80.0% equals"
    assert Link.objects.first().relationship == "60.0% before"
