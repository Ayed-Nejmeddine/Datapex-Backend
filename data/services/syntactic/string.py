from data.services.syntactic.interfaces import StringInterface
import numpy as np
from pandas.api.types import is_string_dtype
from data.services.syntactic.utils import model_text


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

    def model_data_frequency(self):
        """ model the data and count the number of occurrences and percentage for the models"""
        df = self.df
        columns = df.columns
        percentages = []
        occurrences = []
        data_model = []
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                modeled_df = df[i].fillna('').apply(model_text)
                percentages.append(modeled_df.value_counts(normalize=True) * 100)
                occurrences.append(modeled_df.value_counts())
                data_model.append(np.array(modeled_df.value_counts().axes))
        return data_model, percentages, occurrences
