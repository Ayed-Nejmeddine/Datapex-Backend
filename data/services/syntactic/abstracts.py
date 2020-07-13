from data.services.syntactic.interfaces import BaseInterface
import numpy as np
import pandas as pd
from pandas.api.types import is_string_dtype, is_bool_dtype, is_datetime64_any_dtype


class BaseAbstract(BaseInterface):
    """ contains services for the BaseInterface """

    def compute_null_values(self, file):
        """ indicator of number of NULL values"""
        with file.file.open('r') as f:
            df = pd.DataFrame(pd.read_csv(f))
            df = df.convert_dtypes()
            res = pd.isnull(df).sum()
        return np.array(res)

    def compute_not_null_values(self, file):
        """ indicator of number of NOT NULL values"""
        with file.file.open('r') as f:
            df = pd.DataFrame(pd.read_csv(f))
            df = df.convert_dtypes()
            res = df.count()
        return np.array(res)

    def compute_distinct_values(self, file):
        """ indicator of number of distinct values."""
        with file.file.open('r') as f:
            df = pd.DataFrame(pd.read_csv(f))
            df = df.convert_dtypes()
            res = np.array(df.nunique())
        return res

    def compute_unique_values(self, file):
        """ indicator of number of unique values."""
        with file.file.open('r') as f:
            df = pd.DataFrame(pd.read_csv(f))
            df = df.convert_dtypes()
            columns = df.columns
            res = np.zeros(len(columns), dtype=int)
            for i in columns:
                res[columns.get_loc(i)] = len(df[i].drop_duplicates(keep=False))
        return res

    def compute_duplicated_values(self, file):
        """ indicator of number of duplicated values."""
        res = self.compute_distinct_values(file) - self.compute_unique_values(file)
        return res

    def compute_number_of_words(self, file):
        """ indicator of number of words."""
        with file.file.open('r') as f:
            df = pd.DataFrame(pd.read_csv(f))
            df = df.convert_dtypes()
            columns = df.columns
            res = np.zeros(len(columns), dtype=int)
            for i in columns:
                if is_string_dtype(df[i].dtypes):
                    res[columns.get_loc(i)] = df[i].fillna('').str.split().apply(len).sum()
        return res

    def compute_number_of_number_type_values(self, file):
        """indicator of Number of values of the NUMBER TYPE."""
        with file.file.open('r') as f:
            df = pd.DataFrame(pd.read_csv(f))
            df = df.convert_dtypes()
            res = df.apply(pd.to_numeric, errors='coerce').count()
            return np.array(res)

    def compute_number_of_different_values(self, file):
        """ indicator of Number of DIFFERENT values. """
        with file.file.open('r') as f:
            df = pd.DataFrame(pd.read_csv(f))
            df = df.convert_dtypes()
            columns = df.columns
            res = np.zeros(len(columns), dtype=int)
            for i in columns:
                res[columns.get_loc(i)] = df[i].value_counts().count()
        return res

    def compute_number_of_null_type_values(self, file):
        """ indicator of number of null type values."""
        with file.file.open('r') as f:
            df = pd.DataFrame(pd.read_csv(f))
            df = df.convert_dtypes()
            res = df.isnull().sum()
        return np.array(res)

    def compute_number_of_boolean_type_values(self, file):
        """ indicator of number of boolean type values """
        with file.file.open('r') as f:
            df = pd.DataFrame(pd.read_csv(f))
            df = df.convert_dtypes()
            columns = df.columns
            res = np.zeros(len(columns), dtype=int)
            for i in columns:
                if is_bool_dtype(df[i].dtypes):
                    res[columns.get_loc(i)] = df[i].count()
        return res

    def compute_number_of_string_type_values(self, file):
        """ String type indicator."""
        with file.file.open('r') as f:
            df = pd.DataFrame(pd.read_csv(f))
            df = df.convert_dtypes()
            columns = df.columns
            res = np.zeros(len(columns), dtype=int)
            for i in columns:
                if is_string_dtype(df[i].dtypes):
                    res[columns.get_loc(i)] = df[i].count()
        return res

    def compute_number_of_date_type_values(self, file):
        """ Datetime type indicator. """
        with file.file.open('r') as f:
            df = pd.DataFrame(pd.read_csv(f))
            df = df.convert_dtypes()
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

    def compute_model_data_frequency(self, file):
        """ model data frequency."""
        # TODO: model data frequency  # pylint: disable=W0511
        pass
