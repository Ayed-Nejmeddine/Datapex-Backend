from data.services.syntactic.interfaces import StringInterface
import numpy as np
from pandas.api.types import is_string_dtype
from data.services.syntactic.utils import model_text, get_regexp
from data.models.basic_models import SyntacticResult, AnalysisTrace
from threading import Thread
from data.models import STRING_ANALYSIS, FINISHED_STATE


class StringAnalyser(StringInterface, Thread):
    """ contains services for StringInterface """
    def __init__(self, df, document_id):
        self.df = df
        self.document_id = document_id
        Thread.__init__(self)

    def get_min_length(self):
        """ indicator for min length"""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].fillna('').str.len().min()
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule='M102 [17]',
                                                 defaults={'result':{i: res[self.df.columns.get_loc(i)] for i in self.df.columns}})
        return res

    def get_max_length(self):
        """ indicator for max length"""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].fillna('').str.len().max()
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule='M103 [18]',
                                                 defaults={'result':{i: res[self.df.columns.get_loc(i)] for i in self.df.columns}})
        return res

    def get_average_length(self):
        """ indicator for average length"""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].fillna('').str.len().mean()
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule='M104 [19]',
                                                 defaults={'result':{i: res[self.df.columns.get_loc(i)] for i in self.df.columns}})
        return res

    def count_number_of_words(self, s=' '):
        """ indicator of number of words."""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].fillna('').str.split(s).apply(len).sum()
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule='M105 [8]',
                                                 defaults={'result':{i: res[self.df.columns.get_loc(i)] for i in self.df.columns}})
        return res

    def count_values(self):
        """ String type indicator."""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].count()
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule='M108 [11]',
                                                 defaults={'result':{i: res[self.df.columns.get_loc(i)] for i in self.df.columns}})
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
            else:
                data_model.append('None')
                occurrences.append(0)
                percentages.append(0)

        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule='M107 [10]',
                                                 defaults={'result':{i: data_model[columns.get_loc(i)] for i in columns}})
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule='M106 [9]',
                                                 defaults={'result':[{i: occurrences[columns.get_loc(i)] for i in columns},
                                                                     {i: percentages[columns.get_loc(i)] for i in columns}]})

        return data_model, percentages, occurrences

    def syntactic_validation_with_regexp(self, invalid=False):
        """ Syntaxically validate the data according to the regular expressions in the model RegularExp"""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].apply(get_regexp).count()
        if invalid:
            res = np.array(df.shape[0]) - res
        return res

    def run(self):
        self.get_min_length()
        self.get_max_length()
        self.get_average_length()
        self.count_number_of_words()
        self.count_values()
        self.model_data_frequency()
        AnalysisTrace.objects.update_or_create(document_id=self.document_id, analysis_type=STRING_ANALYSIS,
                                               defaults={'state': FINISHED_STATE})
