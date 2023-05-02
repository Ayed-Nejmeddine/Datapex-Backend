"""Here all string tests."""
import numpy as np
import pytest

from data.models import M102_17
from data.models import M103_18
from data.models import M104_19
from data.models import M105_20
from data.models.basic_models import SyntacticResult
from data.services.syntactic import StringAnalyser
from data.services.syntactic import BooleanAnalyser


@pytest.mark.django_db
def test_get_min_length(_element_fixture):
    """Test for min length"""
    service, document = _element_fixture(
        name="test_string.csv", path="test_string.csv", service=StringAnalyser
    )
    res = service.get_min_length()
    expected_result = [3, 0, 4, 7, 0]
    assert np.array_equal(res, expected_result)

    # Check if the result was saved in the database
    syntactic_result = SyntacticResult.objects.get(document=document, rule=M102_17)
    assert syntactic_result.result == {"Name": 3, "Age": 0, "Gender": 4, "City": 7, "Salary": 0}


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
    expected_result = [4, 0, 5, 8, 0]
    assert np.array_equal(res, expected_result)

    # Check if the result was saved in the database
    syntactic_result = SyntacticResult.objects.get(document=document, rule=M104_19)
    assert syntactic_result.result == {"Name": 4, "Age": 0, "Gender": 5, "City": 8, "Salary": 0}


@pytest.mark.django_db
def test_frequency_table(_element_fixture):
    """Test for frequency_table"""
    service, document = _element_fixture(
        name="test_string.csv", path="test_string.csv", service=StringAnalyser
    )
    res = service.frequency_table()
    expected_result = [
        ["Rachel", "Lily", "John", "Emma", "Joe", "Samantha", "George", "Amy", "Oliver", "Lucy"],
        "None",
        [
            "Female",
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
        [
            "New York",
            "Los Angeles",
            "Chicago",
            "Houston",
            "Phoenix",
            "Philadelphia",
            "San Antonio",
            "Phoenix",
            "New York",
            "San Jose",
        ],
        "None",
    ]
    assert np.array_equal(res, expected_result)
    # Check if the result was saved in the database
    syntactic_result = SyntacticResult.objects.get(document=document, rule=M105_20)
    assert syntactic_result.result == {
        "Name": [
            "Rachel",
            "Lily",
            "John",
            "Emma",
            "Joe",
            "Samantha",
            "George",
            "Amy",
            "Oliver",
            "Lucy",
        ],
        "Age": "None",
        "Gender": [
            "Female",
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
            "Phoenix",
            "New York",
            "San Jose",
        ],
        "Salary": "None",
    }


@pytest.mark.django_db
def test_count_boolean_value(_element_fixture):
    """
    Test to count type values
    """
    service, document = _element_fixture(
        name="base_abstract_source.csv", path="base_abstract_source.csv", service=BooleanAnalyser
    )
    res = service.count_boolean_value()

    expected_value = [{'true':0,'false':0},{'true':0,'false':0},{'true':0,'false':0},{'true':0,'false':0},{'true':0,'false':0},{'true':0,'false':0},{'true':0,'false':0},{'true':0,'false':0},{'true':1,'false':1},{'true':7,'false':3},{'true':4,'false':1}]
    assert res == expected_value