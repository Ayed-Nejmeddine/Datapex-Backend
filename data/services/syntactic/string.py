from data.services.syntactic.interfaces import StringInterface
import numpy as np
import pandas as pd
from pandas.api.types import is_string_dtype
from data.services.syntactic.utils import model_text, get_regexp, get_data_dict
from data.models.basic_models import SyntacticResult, AnalysisTrace, DataDict, RegularExp, Link, SemanticData
from threading import Thread
from data.models import STRING_ANALYSIS, FINISHED_STATE, M102_17, M103_18, M104_19, M105_8, M108_11, \
    M107_10, M106_9, M102_25, M103_25, M102_26, M103_26, DATA_TYPES, MATCHED_EXPRESSIONS, COLUMN_TYPE
from fuzzywuzzy import fuzz


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
                                                 defaults={'result': {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}})
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
        invalid_res = np.full(len(columns), np.array(df.shape[0]))
        matched_expressions = []
        percentages = []
        column_type = []
        total_dict = []
        expressions = RegularExp.objects.all().values('expression')
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                reg_exp = df[i].value_counts(dropna=False).keys().to_series().apply(get_regexp, expressions=expressions)
                column_type.append(reg_exp)
                invalid_res[columns.get_loc(i)] = df[i].value_counts(dropna=False)[reg_exp.isna()].sum()
                r = reg_exp.apply(lambda x: ('no-match', 'no-match') if x is None else x)
                matched_dict = {}
                percentage = df[i].value_counts(dropna=False, normalize=True) * 100
                for j in range(len(r)):
                    if r[j] in matched_dict.keys():
                        matched_dict[r[j]] += percentage[j]
                    else:
                        matched_dict[r[j]] = percentage[j]
                matched_expressions.append(matched_dict.keys())
                percentages.append(matched_dict.values())
                total_dict.append(matched_dict)
            else:
                matched_expressions.append(['non-applicable'])
                percentages.append([0])
                column_type.append([])
                total_dict.append({})
        res = np.array(df.shape[0]) - invalid_res
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule=M102_25,
                                                 defaults={'result': {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}})
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule=MATCHED_EXPRESSIONS,
                                                 defaults={'result': {i: (matched_expressions[columns.get_loc(i)],
                                                                          percentages[columns.get_loc(i)]) for i in columns}})
        # the number of syntactically invalid data according to the regular expressions
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule=M103_25,
                                                 defaults={'result': {i: invalid_res[self.df.columns.get_loc(i)] for i in self.df.columns}})
        return column_type, total_dict

    def syntactic_validation_with_data_dict(self):
        """
        Syntactically validate the data according to the data dictionary.
        res is an array of the number of syntactically valid data according to the data dictionary.
        invalid_res is an array of the number of syntactically invalid data according to the data dictionary.
        data_types will contain the data types of each column (exp: city, airport, firstname, etc...) and percentages will contain the percentages of
        the data_types in each column.
        """
        df = self.df
        columns = df.columns
        invalid_res = np.full(len(columns), np.array(df.shape[0]))
        #  TODO: Matching with the data dict takes a long time due to the size of the data_dict.  # pylint: disable=W0511
        data_dict = DataDict.objects.all()
        data_types = []
        percentages = []
        column_type = []
        total_dict = []
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                d = df[i].value_counts(dropna=False).keys().to_series().apply(get_data_dict, data_dict=data_dict)
                column_type.append(d)
                matched_res = d.apply(lambda x: ('no-match', 'no-match') if x is None else x)
                matched_dict = {}
                percentage = df[i].value_counts(dropna=False, normalize=True) * 100
                for j in range(len(matched_res)):
                    if matched_res[j] in matched_dict.keys():
                        matched_dict[matched_res[j]] += percentage[j]
                    else:
                        matched_dict[matched_res[j]] = percentage[j]

                data_types.append(matched_dict.keys())
                percentages.append(matched_dict.values())
                total_dict.append(matched_dict)
                invalid_res[columns.get_loc(i)] = df[i].value_counts(dropna=False)[d.isna()].sum()
            else:
                data_types.append(['non-applicable'])
                percentages.append([0])
                column_type.append([])
                total_dict.append({})
        res = np.array(df.shape[0]) - invalid_res
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule=M102_26,
                                                 defaults={'result': {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}})
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule=DATA_TYPES,
                                                 defaults={'result': {i: (data_types[columns.get_loc(i)],
                                                                          percentages[columns.get_loc(i)]) for i in columns}})
        # number of syntactically invalid data according to the data dictionary
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule=M103_26,
                                                 defaults={'result': {i: invalid_res[self.df.columns.get_loc(i)] for i in self.df.columns}})
        return column_type, total_dict

    def get_columns_type(self):
        """ Get an estimate of the column type """
        data_column_type, data_matching_dict = self.syntactic_validation_with_data_dict()
        regexp_column_type, regexp_matching_dict = self.syntactic_validation_with_regexp()
        matched_res = []
        res_types = []
        for i in range(len(regexp_column_type)):
            res = []
            most_matched_reg = max(regexp_matching_dict[i], key=regexp_matching_dict[i].get)
            most_matched_data = max(data_matching_dict[i], key=data_matching_dict[i].get)
            if most_matched_reg == ('no-match', 'no-match'):
                res.append(most_matched_data)
                res_types.append('datadict')
            else:
                res.append(most_matched_reg)
                res_types.append('regexp')
            matched_res.append(res)
        SemanticData.objects.update_or_create(document_id=self.document_id, defaults={'data': {i: res_types[self.df.columns.get_loc(i)] for i in self.df.columns}})
        SyntacticResult.objects.update_or_create(document_id=self.document_id, rule=COLUMN_TYPE,
                                                 defaults={'result': {i: matched_res[self.df.columns.get_loc(i)] for i in self.df.columns}})

    def link(self):
        """
        Define the links between columns of the type string by calculating the rate of similarity between these columns.
        For example two columns with identical values have a similarity score of 100%.
        """
        df = self.df
        columns = df.columns
        for col1 in columns:
            for col2 in columns[columns.get_loc(col1) + 1:]:
                s = df[col1].apply(fuzz.token_set_ratio, s2=df[col2]).mean()
                if is_string_dtype(df[col1].dtypes) and is_string_dtype(df[col2].dtypes) and s > 80:
                    Link.objects.update_or_create(document_id=self.document_id,
                                                  first_column=col1,
                                                  second_column=col2,
                                                  defaults={'relationship': str(s)+'% similarity score'})

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
        self.link()
