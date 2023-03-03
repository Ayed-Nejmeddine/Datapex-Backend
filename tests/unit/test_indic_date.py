"""Here all date tests."""
import numpy as np
import pytest

from data.services.syntactic.date import DateAnalyser


@pytest.mark.django_db
def test_date_format_mm_dd_yyyy(base_element, d_f):
    """tests the date format : mm dd yyyy"""
    base_element_date = base_element(
        name="Days_test", path="Days.csv", d_f=d_f, service=DateAnalyser
    )
    expected_result = [0, 0, 0, 0, 0, 0, 0, 1, 0]
    result = base_element_date.check_format_dataframe("M112", ["%m %d %Y"])
    assert np.array_equal(expected_result, result)


@pytest.mark.django_db
def test_date_format_mm_dd_yy(base_element, d_f):
    """tests the date format : mm dd yy"""
    base_element_date = base_element(
        name="Days_test", path="Days.csv", d_f=d_f, service=DateAnalyser
    )
    expected_result = [0, 0, 0, 0, 0, 0, 0, 1, 0]
    result = base_element_date.check_format_dataframe("M113", ["%m %d %y"])
    assert np.array_equal(expected_result, result)


# will be changed
@pytest.mark.django_db
def test_date_format_dd_mmm_yyyy(base_element, d_f):
    """tests the date format : dd mmm yyyy"""
    base_element_date = base_element(
        name="Days_test", path="Days.csv", d_f=d_f, service=DateAnalyser
    )
    expected_result = [0, 0, 0, 0, 0, 0, 2, 0, 0]
    result = base_element_date.check_format_dataframe("M114", ["%d %b %Y"])
    assert np.array_equal(expected_result, result)


@pytest.mark.django_db
def test_date_format_french_date(base_element, d_f):
    """tests the date format : french date"""
    base_element_date = base_element(
        name="Days_test", path="Days.csv", d_f=d_f, service=DateAnalyser
    )
    expected_result = [0, 0, 0, 0, 0, 0, 1, 4, 0]
    result = base_element_date.check_format_dataframe("M115", ["%d/%m/%Y"])
    assert np.array_equal(expected_result, result)


@pytest.mark.django_db
def test_date_format_24_hour_time(base_element, d_f):
    """tests the date format : 24 hour time"""
    base_element_date = base_element(
        name="Days_test", path="Days.csv", d_f=d_f, service=DateAnalyser
    )
    expected_result = [0, 0, 0, 0, 0, 0, 0, 1, 0]
    result = base_element_date.check_format_dataframe("M117", ["%H:%M:%S"])
    assert np.array_equal(expected_result, result)


@pytest.mark.django_db
def test_date_format_iso_date(base_element, d_f):
    """tests the date format : iso date"""
    base_element_date = base_element(
        name="Days_test", path="Days.csv", d_f=d_f, service=DateAnalyser
    )
    expected_result = [0, 0, 0, 0, 0, 0, 0, 2, 1]
    result = base_element_date.check_format_dataframe("M116", ["%Y/%m/%d", "%Y-%m-%d"])
    assert np.array_equal(expected_result, result)


@pytest.mark.django_db
def test_date_format_date_time_mm_dd_yyyy_hh_mm(base_element, d_f):
    """tests the date format : mm dd yyyy hh mm"""
    base_element_date = base_element(
        name="Days_test", path="Days.csv", d_f=d_f, service=DateAnalyser
    )
    expected_result = [0, 0, 0, 0, 0, 0, 1, 0, 2]
    result = base_element_date.check_format_dataframe("M118", ["%m/%d/%Y %H:%M"])
    assert np.array_equal(expected_result, result)


@pytest.mark.django_db
def test_date_format_date_time_mm_dd_yyyy_hh_mm_ss(base_element, d_f):
    """tests the date format : mm dd yyyy hh mm ss"""
    base_element_date = base_element(
        name="Days_test", path="Days.csv", d_f=d_f, service=DateAnalyser
    )
    expected_result = [0, 0, 0, 0, 0, 0, 2, 0, 0]
    result = base_element_date.check_format_dataframe("M119", ["%m/%d/%Y %H:%M:%S"])
    assert np.array_equal(expected_result, result)


@pytest.mark.django_db
def test_date_format_month(base_element, d_f):
    """tests the date format : month"""
    base_element_date = base_element(
        name="Days_test", path="Days.csv", d_f=d_f, service=DateAnalyser
    )
    expected_result = [0, 0, 0, 0, 0, 0, 2, 0, 1]
    result = base_element_date.check_format_dataframe("M120", ["%B"])
    assert np.array_equal(expected_result, result)


@pytest.mark.django_db
def test_date_format_week_day(base_element, d_f):
    """tests the date format : week day"""
    base_element_date = base_element(
        name="Days_test", path="Days.csv", d_f=d_f, service=DateAnalyser
    )
    expected_result = [7, 6, 6, 5, 7, 6, 0, 0, 1]
    result = base_element_date.check_format_dataframe("M121", ["%A", "%a"])
    assert np.array_equal(expected_result, result)
