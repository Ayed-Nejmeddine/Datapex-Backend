from data.services.syntactic.interfaces import StringInterface
import numpy as np
from pandas.api.types import is_string_dtype


class StringAnalyser(StringInterface):
    """ contains services for StringInterface """
    def __init__(self, df):
        self.df = df

    def get_min_length(self):
        """ indicator for min length"""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].fillna('').str.len().min()
        return res

    def get_max_length(self):
        """ indicator for max length"""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].fillna('').str.len().max()
        return res

    def get_average_length(self):
        """ indicator for average length"""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].fillna('').str.len().mean()
        return res

    def count_number_of_words(self, s=' '):
        """ indicator of number of words."""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].fillna('').str.split(s).apply(len).sum()
        return res

    def count_values(self):
        """ String type indicator."""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].count()
        return res
