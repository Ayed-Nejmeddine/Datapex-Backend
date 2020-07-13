from data.services.syntactic.interfaces import StringInterface
import numpy as np
import pandas as pd
from pandas.api.types import is_string_dtype


class StringAbstract(StringInterface):
    """ contains services for StringInterface """

    def compute_min_length(self, file):
        """ indicator for min length"""
        with file.file.open('r') as f:
            df = pd.DataFrame(pd.read_csv(f))
            df = df.convert_dtypes()
            columns = df.columns
            res = np.zeros(len(columns), dtype=int)
            for i in columns:
                if is_string_dtype(df[i].dtypes):
                    res[columns.get_loc(i)] = df[i].fillna('').str.len().min()
        return res

    def compute_max_length(self, file):
        """ indicator for max length"""
        with file.file.open('r') as f:
            df = pd.DataFrame(pd.read_csv(f))
            df = df.convert_dtypes()
            columns = df.columns
            res = np.zeros(len(columns), dtype=int)
            for i in columns:
                if is_string_dtype(df[i].dtypes):
                    res[columns.get_loc(i)] = df[i].fillna('').str.len().max()
        return res

    def compute_average_length(self, file):
        """ indicator for average length"""
        with file.file.open('r') as f:
            df = pd.DataFrame(pd.read_csv(f))
            df = df.convert_dtypes()
            columns = df.columns
            res = np.zeros(len(columns), dtype=int)
            for i in columns:
                if is_string_dtype(df[i].dtypes):
                    res[columns.get_loc(i)] = df[i].fillna('').str.len().mean()
        return res
