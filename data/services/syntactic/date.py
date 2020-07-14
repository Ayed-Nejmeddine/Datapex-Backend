from data.services.syntactic.interfaces import DateInterface
import pandas as pd
from data.services.syntactic.utils import check_format
import numpy as np
from pandas.api.types import is_string_dtype


class DateAbstract(DateInterface):
    """ contains services for DateInterface """
    def __init__(self, file):
        with file.file.open('r') as f:
            df = pd.DataFrame(pd.read_csv(f))
            self.df = df.convert_dtypes()

    def check_format_for_dataframe(self, file, format='%m-%d-%Y'):
        """ For a given format, an array of booleans is returned where each value reflects the
        existence of a date according to this format in the corresponding column."""
        df = self.df
        columns = df.columns
        res = np.full(len(columns), False)
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].fillna('').apply(check_format, format=format).all()
        return res
