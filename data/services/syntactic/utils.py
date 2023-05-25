"""Here all the utils functions"""
import datetime
import json
import re

import pandas as pd

from data.models import DAYS_TRANSLATOR
from data.models import MONTHS_TRANSLATOR


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
    text = str(text).strip().lower()
    return text in ["true", "false"]


def check_lower_case(text):
    """check if string contains a bool"""
    return str(text).islower()


def model_text(text):
    """replace the characters in a string with 'A'"""
    res = ""
    for i in text.split():
        if bool(res):
            res += " " + "A" * len(i)
        else:
            res += "A" * len(i)
    return res


def get_regexp(value, expressions):
    """Get the matching regular expression."""
    if not pd.isnull(value):
        for exp in expressions:
            if isinstance(value, str):
                cat = re.search(exp[2], value.upper())
                if cat:
                    return (exp[0], exp[1])
            elif not isinstance(value, bool):
                cat = re.search(exp[2], str(value))
                if cat:
                    return (exp[0], exp[1])
    return ("no-match", "no-match")


def get_data_dict(text, data_dict):
    """Get the matching data dictionary."""
    if not pd.isnull(text):
        text = " ".join(text.split())
        for data in data_dict:
            if text.upper() in data.data_dict:
                json_data_dict = json.loads(data.data_dict)
                for row in json_data_dict:
                    for sub, val in row.items():
                        if text.upper() == val:
                            return (row["CATEGORY"], sub)

    return ("no-match", "no-match")


def verify_Uppercase(text):
    """Verify if the text is uppercase"""
    if text.isupper():
        return 1

    return 0


def verify_MixCasse(text):
    """Verify if the text is MixCasse"""
    if re.search(r"[A-Z]", text) and re.search(r"[a-z]", text):
        return 1
    return 0
