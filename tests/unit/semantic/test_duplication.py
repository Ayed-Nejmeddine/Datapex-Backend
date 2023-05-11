import numpy as np
import pytest
from data.services.semantic import SemanticAnalyser


@pytest.mark.django_db
def test_remove_duplicates(_semantic_doc_analyser_fixture):
    """
    Test remove_duplicates
    """
    doc = _semantic_doc_analyser_fixture
    print(doc.remove_duplicates())
    

