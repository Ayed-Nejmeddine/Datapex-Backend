from data.services.syntactic.interfaces import DateInterface
from data.services.syntactic.utils import check_format
import numpy as np
import pandas as pd
from pandas.api.types import is_string_dtype, is_datetime64_any_dtype
from data.models.basic_models import SyntacticResult, AnalysisTrace
from threading import Thread
from data.models import DATE_ANALYSIS, FINISHED_STATE


class DateAnalyser(DateInterface, Thread):
    """ contains services for DateInterface """

    def __init__(self, df, document_id):
        self.df = df
        self.document_id = document_id
        Thread.__init__(self)

    def check_format_for_dataframe(self, rule, date_format=['%m-%d-%Y']):
        """ For a given format, an array of booleans is returned where each value reflects the
        existence of a date according to this format in the corresponding column."""
        df = self.df
        columns = df.columns
        res = np.full(len(columns), False)
        for date_for in date_format:
            for i in columns:
                if is_string_dtype(df[i].dtypes):
                    res[columns.get_loc(i)] += df[i].fillna('').apply(check_format, date_format=date_for).any()
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule=rule,
                                                 defaults={'result':{i: res[self.df.columns.get_loc(i)] for i in self.df.columns}})
        return res

    def count_values(self):
        """ Datetime type indicator. """
        rule = 'M110 [13]'
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(df[i].dtypes) or is_datetime64_any_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].apply(pd.to_datetime, errors='coerce').count()
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule=rule,
                                                 defaults={'result':{i: res[self.df.columns.get_loc(i)] for i in self.df.columns}})
        return res

    def run(self):
        self.count_values()
        self.check_format_for_dataframe(rule='M112', date_format=['%m/%d/%Y', '%m-%d-%Y'])
        self.check_format_for_dataframe(rule='M113', date_format=['%m/%d/%y', '%m-%d-%y'])
        self.check_format_for_dataframe(rule='M114', date_format=['%d/%b/%Y', '%d-%b-%Y', '%d %b %Y'])
        self.check_format_for_dataframe(rule='M115', date_format=['%d/%m/%Y', '%d-%m-%Y'])
        self.check_format_for_dataframe(rule='M116', date_format=['%Y/%m/%d', '%Y-%m-%d'])
        self.check_format_for_dataframe(rule='M117', date_format=['%H:%M', '%H:%M:%S'])
        self.check_format_for_dataframe(rule='M118', date_format=['%m/%d/%Y %H:%M'])
        self.check_format_for_dataframe(rule='M119', date_format=['%m/%d/%Y %H:%M:%S'])
        self.check_format_for_dataframe(rule='M120', date_format=['%B'])
        self.check_format_for_dataframe(rule='M121', date_format=['%A', '%a'])
        AnalysisTrace.objects.update_or_create(document_id=self.document_id, analysis_type=DATE_ANALYSIS,
                                               defaults={'state': FINISHED_STATE})
