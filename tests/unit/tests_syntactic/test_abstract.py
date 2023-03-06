import numpy as np
import pytest


@pytest.mark.django_db
def test_count_null_type_values(_abstract_document_fixture):
    result = _abstract_document_fixture.count_null_values_by_type()
    expected_result = np.array([0, 0, 0, 2], dtype=object)
    assert np.array_equal(result, expected_result)
