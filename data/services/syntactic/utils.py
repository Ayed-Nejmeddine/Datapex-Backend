import datetime
import numpy as np
from pandas.api.types import is_string_dtype


def check_format(date_text, format='%Y-%m-%d'):
    """ check if a string contains a date with a given format"""
    try:
        datetime.datetime.strptime(date_text, format)
        return True
    except ValueError:
        return False
    return


def check_format_for_dataframe(df, format='%Y-%m-%d'):
    """ check if a given format exists in a dataframe"""
    columns = df.columns
    res = np.full(len(columns), False)
    for i in columns:
        if is_string_dtype(df[i].dtypes):
            res[columns.get_loc(i)]= df[i].fillna('').apply(check_format,format=format).all()
    return res

