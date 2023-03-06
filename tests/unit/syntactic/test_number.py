"""Here test number"""
import numpy as np
import pytest


@pytest.mark.django_db
def test_compute_min_value(_number_document_fixture):
    """Test compute min value."""
    # Call the compute_min_value() function and get the actual result
    result = _number_document_fixture.compute_min_value()
    # Define the expected result
    # convert expected result to the same data type as the result
    expected_result = np.array([1, "non-applicable", 1.1, "non-applicable"], dtype=object)
    # Verify the actual result is equal to the expected result
    assert np.array_equal(result, expected_result)


@pytest.mark.django_db
def test_compute_max_value(_number_document_fixture):
    """Test compute max value."""
    # Call the compute_max_value() function and get the actual result
    result = _number_document_fixture.compute_max_value()
    # convert expected result to the same data type as the result
    expected_result = np.array([3, "non-applicable", 4.4, "non-applicable"], dtype=object)
    # Verify the actual result is equal to the expected result
    assert np.array_equal(result, expected_result)


@pytest.mark.django_db
def test_compute_average_value(_number_document_fixture):
    """Test compute average value."""
    # Call the compute_average_value() function and get the actual result
    result = _number_document_fixture.compute_average_value()
    # convert expected result to the same data type as the result
    expected_result = np.array([2, "non-applicable", 2.75, "non-applicable"], dtype=object)
    # Verify the actual result is equal to the expected result
    assert np.array_equal(result, expected_result)


@pytest.mark.django_db
def test_compute_mode_value(_number_document_fixture):
    """Test compute mode value."""
    # Call the compute_mode_value() function and get the actual result
    result = _number_document_fixture.compute_mode_value()
    # convert expected result to the same data type as the result
    expected_result = np.array([2, "non-applicable", 1.1, "non-applicable"], dtype=object)
    # Verify the actual result is equal to the expected result
    assert np.array_equal(result, expected_result)


@pytest.mark.django_db
def test_compute_median_value(_number_document_fixture):
    """Test compute median value."""
    # Call the compute_median_value() function and get the actual result
    result = _number_document_fixture.compute_median_value()
    # convert expected result to the same data type as the result
    expected_result = np.array([2, "non-applicable", 2.75, "non-applicable"], dtype=object)
    # Verify the actual result is equal to the expected result
    assert np.array_equal(result, expected_result)


@pytest.mark.django_db
def test_count_values_number(_number_document_fixture):
    """Test count values number."""
    # Call the count_values() function and get the actual result
    result = _number_document_fixture.count_values()
    # Define the expected result
    expected_result = [4, 0, 4, 0]
    # Verify the actual result is equal to the expected result
    assert np.array_equal(result, expected_result)
