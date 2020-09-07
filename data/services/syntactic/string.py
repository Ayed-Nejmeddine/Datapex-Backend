from data.services.syntactic.interfaces import StringInterface
import numpy as np
from pandas.api.types import is_string_dtype
from data.services.syntactic.utils import model_text, get_regexp, get_data_dict
from data.models.basic_models import SyntacticResult, AnalysisTrace, DataDict, RegularExp
from threading import Thread
from data.models import STRING_ANALYSIS, FINISHED_STATE, M102_17, M103_18, M104_19, M105_8, M108_11, \
    M107_10, M106_9, M102_25, M103_25, M102_26, M103_26, DATA_TYPES, MATCHED_EXPRESSIONS, COLUMN_TYPE


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
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule=M102_17,
                                                 defaults={'result': {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}})
        return res

    def get_max_length(self):
        """ indicator for max length"""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].fillna('').str.len().max()
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule=M103_18,
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
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule=M104_19,
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
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule=M105_8,
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
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule=M108_11,
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

        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule=M107_10,
                                                 defaults={'result':{i: data_model[columns.get_loc(i)] for i in columns}})
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule=M106_9,
                                                 defaults={'result':{i: (occurrences[columns.get_loc(i)], percentages[columns.get_loc(i)]) for i in columns}})

        return data_model, percentages, occurrences

    def syntactic_validation_with_regexp(self):
        """
        Syntaxically validate the data according to the regular expressions in the model RegularExp.
        res will be an array of the number of syntactically valid data according to the regular expressions.
        invalid_res will be an array of the number of syntactically invalid data according to the regular expressions.
        """
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        matched_expressions = []
        percentages = []
        expressions = RegularExp.objects.all().values('expression')
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                reg_exp = df[i].apply(get_regexp, expressions=expressions).fillna('no-match')
                res[columns.get_loc(i)] = reg_exp.count()
                matched_expressions.append(reg_exp.value_counts().keys())
                percentages.append(reg_exp.value_counts(normalize=True) * 100)
            else:
                matched_expressions.append(['non-applicable'])
                percentages.append([0])
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule=M102_25,
                                                 defaults={'result': {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}})
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule=MATCHED_EXPRESSIONS,
                                                 defaults={'result': {i: (matched_expressions[columns.get_loc(i)],
                                                                          percentages[columns.get_loc(i)]) for i in columns}})
        # the number of syntactically invalid data according to the regular expressions
        invalid_res = np.array(df.shape[0]) - res
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule=M103_25,
                                                 defaults={'result': {i: invalid_res[self.df.columns.get_loc(i)] for i in self.df.columns}})
        return matched_expressions, percentages

    def syntactic_validation_with_data_dict(self):
        """
        Syntactically validate the data according to the data dictionary.
        res is an array of the number of syntactically valid data according to the data dictionary.
        invalid_res is an array of the number of syntactically invalid data according to the data dictionary.
        data_types will contain the data types of each column (exp: city, airportn firstame, etc...) and percentages will contain the percentages of
        the data_types in each column.
        """
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        #  TODO: Matching with the data dict takes a long time due to the size of the data_dict.  # pylint: disable=W0511
        data_dict = DataDict.objects.all()
        data_types = []
        percentages = []
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                d = df[i].apply(get_data_dict, data_dict=data_dict).fillna('no-match')
                data_types.append(d.value_counts().keys())
                percentages.append(d.value_counts(normalize=True) * 100)
                res[columns.get_loc(i)] = d.count()
            else:
                data_types.append(['non-applicable'])
                percentages.append([0])
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule=M102_26,
                                                 defaults={'result':{i: res[self.df.columns.get_loc(i)] for i in self.df.columns}})
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule=DATA_TYPES,
                                                 defaults={'result': {i: (data_types[columns.get_loc(i)],
                                                                          percentages[columns.get_loc(i)]) for i in columns}})
        # number of syntactically invalid data according to the data dictionary
        invalid_res = np.array(df.shape[0]) - res
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule=M103_26,
                                                 defaults={'result': {i: invalid_res[self.df.columns.get_loc(i)] for i in self.df.columns}})
        return data_types, percentages

    def get_columns_type(self):
        """ Get an estimate of the column type """
        data_types, data_percentages = self.syntactic_validation_with_data_dict()
        expressions, exp_percentages = self.syntactic_validation_with_regexp()
        res = []
        for i in range(len(data_percentages)):
            if data_types[i][0] == 'no-match' and expressions[i][0] != 'no-match':
                res.append(expressions[i][0])
            elif data_types[i][0] != 'no-match' and expressions[i][0] == 'no-match':
                res.append(data_types[i][0])
            elif data_types[i][0] != 'no-match' and expressions[i][0] != 'no-match':
                if data_percentages[i][0] >= exp_percentages[i][0]:
                    res.append(data_types[i][0])
                else:
                    res.append(expressions[i][0])
            elif data_percentages[i][0] == 100 and exp_percentages[i][0] == 100:
                res.append(expressions[i][0])
            elif exp_percentages[i][0] == 100:
                res.append(data_types[i][1])
            elif data_percentages[i][0] == 100:
                res.append(expressions[i][1])
            else:
                if data_percentages[i][1] >= exp_percentages[i][1]:
                    res.append(data_types[i][1])
                else:
                    res.append(expressions[i][1])
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule=COLUMN_TYPE,
                                                 defaults={'result': {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}})

    def run(self):
        self.get_min_length()
        self.get_max_length()
        self.get_average_length()
        self.count_number_of_words()
        self.count_values()
        self.model_data_frequency()
        self.get_columns_type()
        AnalysisTrace.objects.update_or_create(document_id=self.document_id, analysis_type=STRING_ANALYSIS,
                                               defaults={'state': FINISHED_STATE})
