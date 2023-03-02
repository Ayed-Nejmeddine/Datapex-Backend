"""Here all string tests."""
import numpy as np
import pytest

from data.models import M102_17
from data.models import M103_18
from data.models import M104_19
from data.models import M105_20
from data.models.basic_models import SyntacticResult
from data.services.syntactic import StringAnalyser


@pytest.mark.django_db
def test_get_min_length(_element_fixture):
    """Test for min length"""
    service, document = _element_fixture(
        name="test_string.csv", path="test_string.csv", service=StringAnalyser
    )
    res = service.get_min_length()
    expected_result = [3, 0, 4, 6, 0]
    assert np.array_equal(res, expected_result)

    # Check if the result was saved in the database
    syntactic_result = SyntacticResult.objects.get(document=document, rule=M102_17)
    assert syntactic_result.result == {"Name": 3, "Age": 0, "Gender": 4, "City": 6, "Salary": 0}


@pytest.mark.django_db
def test_get_max_length(_element_fixture):
    """Test for max length"""
    service, document = _element_fixture(
        name="test_string.csv", path="test_string.csv", service=StringAnalyser
    )
    res = service.get_max_length()
    expected_result = [8, 0, 6, 12, 0]
    assert np.array_equal(res, expected_result)

    # Check if the result was saved in the database
    syntactic_result = SyntacticResult.objects.get(document=document, rule=M103_18)
    assert syntactic_result.result == {"Name": 8, "Age": 0, "Gender": 6, "City": 12, "Salary": 0}


@pytest.mark.django_db
def test_get_average_length(_element_fixture):
    """Test for average length"""
    service, document = _element_fixture(
        name="test_string.csv", path="test_string.csv", service=StringAnalyser
    )
    res = service.get_average_length()
    expected_result = [5, 0, 5, 8, 0]
    assert np.array_equal(res, expected_result)

    # Check if the result was saved in the database
    syntactic_result = SyntacticResult.objects.get(document=document, rule=M104_19)
    assert syntactic_result.result == {"Name": 5, "Age": 0, "Gender": 5, "City": 8, "Salary": 0}


@pytest.mark.django_db
def test_frequency_table(_element_fixture):
    """Test for frequency_table"""
    service, document = _element_fixture(
        name="test_string.csv", path="test_string.csv", service=StringAnalyser
    )
    res = service.frequency_table()
    expected_result = [
        ["John", "Alice", "Bob", "Emma", "David", "Samantha", "George", "Emily", "Oliver", "Lucy"],
        "None",
        ["Male", "Female", "Male", "Female", "Male", "Female", "Male", "Female", "Male", "Female"],
        [
            "New York",
            "Los Angeles",
            "Chicago",
            "Houston",
            "Phoenix",
            "Philadelphia",
            "San Antonio",
            "San Diego",
            "Dallas",
            "San Jose",
        ],
        "None",
    ]
    assert np.array_equal(res, expected_result)
    # Check if the result was saved in the database
    syntactic_result = SyntacticResult.objects.get(document=document, rule=M105_20)
    assert syntactic_result.result == {
        "Name": [
            "John",
            "Alice",
            "Bob",
            "Emma",
            "David",
            "Samantha",
            "George",
            "Emily",
            "Oliver",
            "Lucy",
        ],
        "Age": "None",
        "Gender": [
            "Male",
            "Female",
            "Male",
            "Female",
            "Male",
            "Female",
            "Male",
            "Female",
            "Male",
            "Female",
        ],
        "City": [
            "New York",
            "Los Angeles",
            "Chicago",
            "Houston",
            "Phoenix",
            "Philadelphia",
            "San Antonio",
            "San Diego",
            "Dallas",
            "San Jose",
        ],
        "Salary": "None",
    }
