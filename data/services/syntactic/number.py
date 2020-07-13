from data.services.syntactic.interfaces import NumberInterface
import numpy as np
import pandas as pd


class NumberAbstract(NumberInterface):
    """ contains services for NumberInterface """

    def compute_min_value(self, file):
        """ indicator for min value."""
        with file.file.open('r') as f:
            df = pd.DataFrame(pd.read_csv(f))
            df = df.convert_dtypes()
            res = df.apply(pd.to_numeric, errors='coerce').min()
        return np.array(res)

    def compute_max_value(self, file):
        """ indicator for max value."""
        with file.file.open('r') as f:
            df = pd.DataFrame(pd.read_csv(f))
            df = df.convert_dtypes()
            res = df.apply(pd.to_numeric, errors='coerce').max()
        return np.array(res)

    def compute_average_value(self, file):
        """ indicator for average value."""
        with file.file.open('r') as f:
            df = pd.DataFrame(pd.read_csv(f))
            df = df.convert_dtypes()
            res = df.apply(pd.to_numeric, errors='coerce').mean()
        return np.array(res)

    def compute_mode_value(self, file):
        """ indicator for mode value."""
        with file.file.open('r') as f:
            df = pd.DataFrame(pd.read_csv(f))
            df = df.convert_dtypes()
            res = df.apply(pd.to_numeric, errors='coerce').mode().head(1)
        return np.array(res)

    def compute_median_value(self, file):
        """ indicator for median value."""
        with file.file.open('r') as f:
            df = pd.DataFrame(pd.read_csv(f))
            df = df.convert_dtypes()
            res = df.apply(pd.to_numeric, errors='coerce').median()
        return np.array(res)
