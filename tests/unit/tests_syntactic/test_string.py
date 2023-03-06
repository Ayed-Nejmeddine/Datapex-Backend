import numpy as np
import pytest


@pytest.mark.django_db
def test_get_min_length(_string_document_fixture):
    # Call the get_min_length() function and get the actual result
    result = _string_document_fixture.get_min_length()
    # Define the expected result
    expected_result = [1, 1, 1, 1, 1, 1, 6]
    # Verify the actual result is equal to the expected result
    assert np.array_equal(result, expected_result)


@pytest.mark.django_db
def test_get_max_length(_string_document_fixture):
    # Call the get_max_length() function and get the actual result
    result = _string_document_fixture.get_max_length()
    # Define the expected result
    expected_result = [6, 8, 8, 9, 8, 9, 6]
    # Verify the actual result is equal to the expected result
    assert np.array_equal(result, expected_result)


@pytest.mark.django_db
def test_get_average_length(_string_document_fixture):
    # Call the get_average_length() function and get the actual result
    result = _string_document_fixture.get_average_length()
    # Define the expected result
    expected_result = [3, 4, 3, 4, 3, 4, 6]
    # Verify the actual result is equal to the expected result
    assert np.array_equal(result, expected_result)
