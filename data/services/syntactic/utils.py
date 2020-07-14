import datetime


def check_format(date_text, format='%Y-%m-%d'):
    """ check if a string contains a date with a given format"""
    try:
        datetime.datetime.strptime(date_text, format)
        return True
    except ValueError:
        return False
