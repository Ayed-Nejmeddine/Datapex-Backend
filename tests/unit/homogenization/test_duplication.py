import numpy as np
import pytest
from data.services.homgenization import HomogenizationAnalyser


@pytest.mark.django_db
def test_remove_duplicated_rows(_homogenization_doc_analyser_fixture):
    """
    Test remove_duplicates
    """
    doc = _homogenization_doc_analyser_fixture
    print(doc.remove_duplicated_rows())
    

