"""test duplicated rows"""
import pytest


@pytest.mark.django_db
def test_remove_duplicated_rows(_homogenization_doc_analyser_fixture):
    """
    Test remove_duplicates
    """
    doc = _homogenization_doc_analyser_fixture  # noqa: F841
