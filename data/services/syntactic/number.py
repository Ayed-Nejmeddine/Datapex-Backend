from data.services.syntactic.interfaces import NumberInterface
import numpy as np
import pandas as pd


class NumberAnalyser(NumberInterface):
    """ contains services for NumberInterface """
    def __init__(self, df):
        self.df = df

    def compute_min_value(self):
        """ indicator for min value."""
        res = self.df.apply(pd.to_numeric, errors='coerce').min()
        return np.array(res)

    def compute_max_value(self):
        """ indicator for max value."""
        res = self.df.apply(pd.to_numeric, errors='coerce').max()
        return np.array(res)

    def compute_average_value(self):
        """ indicator for average value."""
        res = self.df.apply(pd.to_numeric, errors='coerce').mean()
        return np.array(res)

    def compute_mode_value(self):
        """ indicator for mode value."""
        res = self.df.apply(pd.to_numeric, errors='coerce').mode().head(1)
        return np.array(res)

    def compute_median_value(self):
        """ indicator for median value."""
        res = self.df.apply(pd.to_numeric, errors='coerce').median()
        return np.array(res)

    def count_values(self):
        """indicator of Number of values of the NUMBER TYPE."""
        df = self.df
        res = df.apply(pd.to_numeric, errors='coerce').count()
        return np.array(res)
