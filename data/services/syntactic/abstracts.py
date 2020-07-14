from data.services.syntactic.interfaces import BaseInterface
import numpy as np
import pandas as pd
from pandas.api.types import is_string_dtype, is_bool_dtype, is_datetime64_any_dtype


class BaseAbstract(BaseInterface):
    """ contains services for the BaseInterface """

    def __init__(self, file):
        with file.file.open('r') as f:
            df = pd.DataFrame(pd.read_csv(f))
            self.df = df.convert_dtypes()

    def count_null_values(self, file, inverse=False):
        """ count the NULL values and the NOT NULL values"""
        df = self.df
        res = pd.isnull(df).sum()
        if inverse:
            res = df.count()
        return np.array(res)

    def count_distinct_values(self, file):
        """ Indicator of the number of distinct values."""
        res = np.array(self.df.nunique())
        return res

    def count_unique_values(self, file):
        """ Indicator of the number of unique values.
        Unique values are the values that exist only once."""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            res[columns.get_loc(i)] = len(df[i].drop_duplicates(keep=False))
        return res

    def count_duplicated_values(self, file):
        """ indicator of number of duplicated values."""
        res = self.count_distinct_values(file) - self.count_unique_values(file)
        return res

    def count_number_of_words(self, file, s=' '):
        """ indicator of number of words."""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].fillna('').str.split(s).apply(len).sum()
        return res

    def count_numeric_values(self, file):
        """indicator of Number of values of the NUMBER TYPE."""
        df = self.df
        res = df.apply(pd.to_numeric, errors='coerce').count()
        return np.array(res)

    def count_the_different_values(self, file):
        """ indicator of Number of DIFFERENT values. """
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            res[columns.get_loc(i)] = df[i].value_counts().count()
        return res

    def count_null_type_values(self, file, null='NULL'):
        """ indicator of number of null type values."""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_bool_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].str.count(null).sum()
        return res

    def count_boolean_type_values(self, file):
        """ indicator of number of boolean type values """
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_bool_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].count()
        return res

    def count_string_type_values(self, file):
        """ String type indicator."""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].count()
        return res

    def count_date_type_values(self, file):
        """ Datetime type indicator. """
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(df[i].dtypes) or is_datetime64_any_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].apply(pd.to_datetime, errors='coerce').count()
        return res

    def compute_data_frequency(self, file):
        """ indicator of data frequency."""
        # TODO: Compute data frequency  # pylint: disable=W0511
        pass

    def model_data_frequency(self, file):
        """ model data frequency."""
        # TODO: model data frequency  # pylint: disable=W0511
        pass
