import datetime
from data.models.basic_models import RegularExp
import re
import pandas as pd


def check_format(date_text, date_format='%Y-%m-%d'):
    """ check if a string contains a date with a given format"""
    try:
        datetime.datetime.strptime(date_text, date_format)
        return True
    except ValueError:
        return False


def check_bool(text):
    """ check if string contains a bool"""
    if text.lower() in ['true', 'false']:
        return True
    else:
        return False


def model_text(text):
    """ replace the characters in a string with 'A' """
    res=''
    for i in text.split():
        if bool(res):
            res += ' ' + 'A' * len(i)
        else:
            res += 'A' * len(i)
    return res


def get_regexp(text):
    """ Get the matching regular expression. """
    if not pd.isnull(text):
        expressions = RegularExp.objects.all().values('expression')
        for exp in expressions:
            pattern = re.compile(exp['expression'])
            if pattern.match(text.upper()):
                return RegularExp.objects.filter(expression=exp['expression'])[0]
    return None
