"""tests of base Indicators"""
import numpy as np
import pytest

from data.services.syntactic import BaseAbstract
from data.services.syntactic.date import DateAnalyser
from data.services.syntactic.string import StringAnalyser


@pytest.mark.django_db
def test_should_return_null_values(base_element, d_f):
    """test the number of null values in each column"""
    base_element_abstract = base_element(
        name="Days_test", path="Days.csv", d_f=d_f, service=BaseAbstract
    )
    expected_result = [2, 3, 3, 4, 2, 3, 1, 0, 0]
    result = base_element_abstract.count_null_values(False)
    assert expected_result == result.tolist()


@pytest.mark.django_db
def test_should_return_distinct_values_in_each_column(base_element, d_f):
    """test the number of distinct values in each column"""
    nbredistcol = [7, 6, 6, 5, 7, 6, 7, 8, 7]
    base_element_abstract = base_element(
        name="Days_test", path="Days.csv", d_f=d_f, service=BaseAbstract
    )
    expected_result = np.array(nbredistcol)
    result = base_element_abstract.count_distinct_values()
    assert np.array_equal(result, expected_result)


@pytest.mark.django_db
def test_should_return_number_of_words(base_element, d_f):
    """tests the number of words in each column"""
    base_element_string = base_element(
        name="Days_test", path="Days.csv", d_f=d_f, service=StringAnalyser
    )
    expected_value = [9, 9, 9, 9, 14, 9, 9, 11, 9]
    result = base_element_string.number_of_words("-")
    assert np.array_equal(result, expected_value)


@pytest.mark.django_db
def test_should_return_number_of_type_string_values(base_element, d_f):
    """tests the number of values having type string"""
    base_element_string = base_element(
        name="Days_test", path="Days.csv", d_f=d_f, service=StringAnalyser
    )
    expected_value = [7, 6, 6, 5, 7, 6, 4, 0, 2]
    result = base_element_string.count_values()
    assert np.array_equal(result, expected_value)


@pytest.mark.django_db
def test_should_return_number_of_type_date_values(base_element, d_f):
    """tests the number of values having type date"""
    base_element_date = base_element(
        name="Days_test", path="Days.csv", d_f=d_f, service=DateAnalyser
    )
    expected_value = [0, 0, 0, 0, 0, 0, 6, 9, 3]
    result = base_element_date.count_values()
    assert np.array_equal(result, expected_value)


@pytest.mark.django_db
def test_should_return_different_values_in_each_column(base_element, d_f):
    """test the number of different values"""
    nbredistcol = [8, 7, 7, 6, 8, 7, 8, 8, 7]
    base_element_abstract = base_element(
        name="Days_test", path="Days.csv", d_f=d_f, service=BaseAbstract
    )
    expected_result = np.array(nbredistcol)
    result = base_element_abstract.count_different_values()
    assert np.array_equal(result, expected_result)
