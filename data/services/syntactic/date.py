from data.services.syntactic.interfaces import DateInterface
from data.services.syntactic.utils import check_format
import numpy as np
from pandas.api.types import is_string_dtype, is_datetime64_any_dtype


class DateAnalyser(DateInterface):
    """ contains services for DateInterface """

    def __init__(self, df):
        self.df = df

    def check_format_for_dataframe(self, date_format='%m-%d-%Y'):
        """ For a given format, an array of booleans is returned where each value reflects the
        existence of a date according to this format in the corresponding column."""
        df = self.df
        columns = df.columns
        res = np.full(len(columns), False)
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].fillna('').apply(check_format, date_format=date_format).all()
        return res

    def count_values(self):
        """ Datetime type indicator. """
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(df[i].dtypes) or is_datetime64_any_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].apply(pd.to_datetime, errors='coerce').count()
        return res
