"""Here all the utils functions"""
import datetime
import re

import pandas as pd

from data.models import DAYS_TRANSLATOR
from data.models import MONTHS_TRANSLATOR
from data.models.basic_models import RegularExp


def translate(text):
    """translate the name of a day or month from any other languages to English"""
    if text.isalpha() or text.replace("-", "").isalpha():
        lower = text.lower()
        for day in DAYS_TRANSLATOR:
            if lower in DAYS_TRANSLATOR[day]:
                return day.lower()
        for month in MONTHS_TRANSLATOR:
            if lower in MONTHS_TRANSLATOR[month]:
                return month.lower()
        return False

    return False


def check_format(date_text, date_format="%Y-%m-%d"):
    """check if a string contains a date with a given format"""
    try:
        date_text_eng = translate(date_text)
        if date_text_eng:
            datetime.datetime.strptime(date_text_eng, date_format)
            return 1
        datetime.datetime.strptime(date_text, date_format)
        return 1
    except ValueError:
        return 0


def check_bool(val):
    """check if a value is a bool"""
    return val in (True, False)


def check_string_contains_bool(text):
    """check if string contains a bool"""
    if isinstance(text, str):
        text = text.strip().lower()
        return text in ["true", "false"]
    return None


def model_text(text):
    """replace the characters in a string with 'A'"""
    res = ""
    for i in text.split():
        if bool(res):
            res += " " + "A" * len(i)
        else:
            res += "A" * len(i)
    return res


def get_regexp(text, expressions):
    """Get the matching regular expression."""
    if not pd.isnull(text):
        for exp in expressions:
            if re.search(exp["expression"], text.upper()):
                res = RegularExp.objects.filter(expression=exp["expression"])[0]
                return res.category, res.subcategory
    return None


def get_data_dict(text, data_dict):
    """Get the matching data dictionary."""
    if not pd.isnull(text):
        text = " ".join(text.split())
        for data in data_dict:
            for sub, val in data.data_dict.items():
                if text.upper() == val:
                    return data.data_dict["CATEGORY"], sub
    return None
