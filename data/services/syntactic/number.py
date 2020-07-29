from data.services.syntactic.interfaces import NumberInterface
import numpy as np
import pandas as pd
from data.models.basic_models import SyntacticResult
from threading import Thread
from data.models.basic_models import AnalysisTrace
from data.models import FINISHED_STATE, NUMBER_ANALYSIS


class NumberAnalyser(NumberInterface, Thread):
    """ contains services for NumberInterface """
    def __init__(self, df, document_id):
        self.df = df
        self.document_id = document_id
        Thread.__init__(self)

    def compute_min_value(self):
        """ indicator for min value."""
        res = self.df.apply(pd.to_numeric, errors='coerce').min()
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule='M102 [20]',
                                                 defaults={'result':{i: res[self.df.columns.get_loc(i)] for i in self.df.columns}})
        return np.array(res)

    def compute_max_value(self):
        """ indicator for max value."""
        res = self.df.apply(pd.to_numeric, errors='coerce').max()
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule='M103 [20]',
                                                 defaults={'result':{i: res[self.df.columns.get_loc(i)] for i in self.df.columns}})
        return np.array(res)

    def compute_average_value(self):
        """ indicator for average value."""
        res = self.df.apply(pd.to_numeric, errors='coerce').mean()
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule='M103 [21]',
                                                 defaults={'result':{i: res[self.df.columns.get_loc(i)] for i in self.df.columns}})
        return np.array(res)

    def compute_mode_value(self):
        """ indicator for mode value."""
        res = self.df.apply(pd.to_numeric, errors='coerce').mode().to_numpy()[0]
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule='M104 [22]',
                                                 defaults={'result':{i: res[self.df.columns.get_loc(i)] for i in self.df.columns}})
        return np.array(res)

    def compute_median_value(self):
        """ indicator for median value."""
        res = self.df.apply(pd.to_numeric, errors='coerce').median()
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule='M105 [23]',
                                                 defaults={'result':{i: res[self.df.columns.get_loc(i)] for i in self.df.columns}})
        return np.array(res)

    def count_values(self):
        """indicator of Number of values of the NUMBER TYPE."""
        df = self.df
        res = df.apply(pd.to_numeric, errors='coerce').count()
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule='M109 [12]',
                                                 defaults={'result':{i: res[self.df.columns.get_loc(i)] for i in self.df.columns}})
        return np.array(res)

    def run(self):
        self.compute_min_value()
        self.compute_max_value()
        self.compute_average_value()
        self.compute_mode_value()
        self.compute_median_value()
        self.count_values()
        AnalysisTrace.objects.update_or_create(document_id=self.document_id, analysis_type=NUMBER_ANALYSIS,
                                               defaults={'state': FINISHED_STATE})