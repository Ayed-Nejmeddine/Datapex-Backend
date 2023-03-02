import datetime
import re

import pandas as pd

from data.models.basic_models import RegularExp


def check_format(date_text, date_format="%Y-%m-%d"):
    """check if a string contains a date with a given format"""
    try:
        datetime.datetime.strptime(date_text, date_format)
        return True
    except ValueError:
        return False


def check_bool(val):
    """check if a value is a bool"""
    return val in (True, False)


def check_string_contains_bool(text):
    """check if string contains a bool"""
    if isinstance(text, str):
        text = text.strip().lower()
        return text in ["true", "false"]


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
        for d in data_dict:
            for sub, val in d.data_dict.items():
                if text.upper() == val:
                    return d.data_dict["CATEGORY"], sub
    return None
