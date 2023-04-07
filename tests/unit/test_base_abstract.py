"""Here all base indicators tests."""
import numpy as np
import pytest


@pytest.mark.django_db
def test_count_null_values(_base_indicator_fixture):
    """
    Test to count null values
    """
    expected_value = [0, 1, 2, 2, 0, 0, 2, 4, 0, 0, 5]
    doc = _base_indicator_fixture
    assert doc.count_null_values().tolist() == expected_value


@pytest.mark.django_db
def test_count_not_null_values(_base_indicator_fixture):
    """
    Test to count not null values
    """
    expected_value = [10, 9, 8, 8, 10, 10, 8, 6, 10, 10, 5]
    doc = _base_indicator_fixture
    assert doc.count_null_values(True).tolist() == expected_value


@pytest.mark.django_db
def test_count_distinct_values(_base_indicator_fixture):
    """
    Test to count distinct values
    """
    expected_value = [8, 3, 5, 7, 7, 9, 6, 3, 10, 2, 2]
    doc = _base_indicator_fixture
    assert doc.count_distinct_values().tolist() == expected_value


@pytest.mark.django_db
def test_count_unique_values(_base_indicator_fixture):
    """
    Test to count unique values
    """
    expected_value = [6, 2, 2, 6, 6, 8, 5, 2, 10, 0, 1]
    doc = _base_indicator_fixture
    assert doc.count_unique_values().tolist() == expected_value


@pytest.mark.django_db
def test_count_duplicated_values(_base_indicator_fixture):
    """
    Test to count duplicated values
    """
    expected_value = [2, 1, 3, 1, 1, 1, 1, 1, 0, 2, 1]
    doc = _base_indicator_fixture
    assert doc.count_duplicated_values().tolist() == expected_value


@pytest.mark.django_db
def test_count_boolean_type_values(_base_indicator_fixture):
    """
    Test to count boolean type values
    """
    expected_value = [0, 0, 0, 0, 0, 0, 0, 0, 2, 10, 5]
    doc = _base_indicator_fixture
    assert doc.count_boolean_type_values().tolist() == expected_value


@pytest.mark.django_db
def test_count_number_rows(_base_indicator_fixture):
    """
    Test to count number of rows
    """
    expected_value = 10
    doc = _base_indicator_fixture
    assert doc.count_number_rows() == expected_value


@pytest.mark.django_db
def test_data_type_value(_base_indicator_fixture):
    """
    Test to count type values
    """
    expected_value = [
        {"string": 100.0, "number": 0.0, "boolean": 0.0, "date": 0.0},
        {"string": 90.0, "number": 0.0, "boolean": 0.0, "date": 0.0},
        {"string": 0.0, "number": 0.0, "boolean": 0.0, "date": 80.0},
        {"string": 80.0, "number": 0.0, "boolean": 0.0, "date": 0.0},
        {"string": 100.0, "number": 0.0, "boolean": 0.0, "date": 0.0},
        {"string": 100.0, "number": 0.0, "boolean": 0.0, "date": 0.0},
        {"string": 80.0, "number": 0.0, "boolean": 0.0, "date": 0.0},
        {"string": 60.0, "number": 0.0, "boolean": 0.0, "date": 0.0},
        {"string": 0.0, "number": 80.0, "boolean": 20.0, "date": 0.0},
        {"string": 0.0, "number": 0.0, "boolean": 100.0, "date": 0.0},
        {"string": 0.0, "number": 0.0, "boolean": 50.0, "date": 0.0},
    ]
    doc = _base_indicator_fixture

    assert doc.data_type_value() == expected_value


@pytest.mark.django_db
def test_count_lowercase_values(_base_indicator_fixture):
    """
    Test to count type values
    """
    doc = _base_indicator_fixture

    expected_value = [0.0, 0.0, 0.0, 0.0, 50.0, 0.0, 0.0, 0.0, 10.0, 0.0, 0.0]
    assert np.array_equal(doc.count_lowercase_values(), expected_value)
