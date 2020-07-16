import datetime


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
