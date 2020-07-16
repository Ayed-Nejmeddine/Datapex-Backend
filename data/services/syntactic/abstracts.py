from data.services.syntactic.interfaces import BaseInterface
import numpy as np
import pandas as pd
from pandas.api.types import is_bool_dtype, is_string_dtype
from data.services.syntactic.utils import check_bool


class BaseAbstract(BaseInterface):
    """ contains services for the BaseInterface """

    def __init__(self, df):
        self.df = df

    def count_null_values(self, inverse=False):
        """ count the NULL values and the NOT NULL values"""
        df = self.df
        res = pd.isnull(df).sum()
        if inverse:
            res = df.count()
        return np.array(res)

    def count_distinct_values(self):
        """ Indicator of the number of distinct values."""
        res = np.array(self.df.nunique())
        return res

    def count_unique_values(self):
        """ Indicator of the number of unique values.
        Unique values are the values that exist only once."""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            res[columns.get_loc(i)] = len(df[i].drop_duplicates(keep=False))
        return res

    def count_duplicated_values(self):
        """ indicator of number of duplicated values."""
        res = self.count_distinct_values() - self.count_unique_values()
        return res

    def count_the_different_values(self):
        """ indicator of Number of DIFFERENT values. """
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            res[columns.get_loc(i)] = df[i].value_counts().count()
        return res

    def count_null_type_values(self, null='NULL'):
        """ indicator of number of null type values."""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_bool_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].str.count(null).sum()
        return res

    def count_boolean_type_values(self):
        """ indicator of number of boolean type values """
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_bool_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].count()
            elif is_string_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].fillna('').apply(check_bool).sum()
        return res

    def compute_data_frequency(self):
        """ indicator of data frequency."""
        # TODO: Compute data frequency  # pylint: disable=W0511
        pass

    def model_data_frequency(self):
        """ model data frequency."""
        # TODO: model data frequency  # pylint: disable=W0511
        pass

    def count_syntactically_valid_values(self, invalid=False):
        """count the number of syntactically valid values"""
        df = self.df
        columns = df.columns
        res = np.array(df.count())
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                num = df[i].apply(pd.to_numeric, errors='coerce').count()
                date = df[i].apply(pd.to_datetime, errors='coerce').count()
                bools = df[i].fillna('').apply(check_bool).sum()
                alph = df[i].str.isalnum().sum() - (bool + num)
                res[columns.get_loc(i)] = max(num, alph, date, bools)

        if invalid:
            res = np.array(df.count()) - res
        return res
