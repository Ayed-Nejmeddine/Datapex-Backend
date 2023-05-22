"""Here all string functions"""
from threading import Thread

import numpy as np
from fuzzywuzzy import fuzz
from pandas.api.types import is_string_dtype

from data.models import COLUMN_TYPE
from data.models import FINISHED_STATE
from data.models import M102_17
from data.models import M103_18
from data.models import M104_19
from data.models import M105_8
from data.models import M105_20
from data.models import M106_9
from data.models import M107_10
from data.models import M108_11
from data.models import STRING_ANALYSIS
from data.models.basic_models import AnalysisTrace
from data.models.basic_models import Link
from data.models.basic_models import SemanticData
from data.models.basic_models import SyntacticResult
from data.services.syntactic import BaseAbstract
from data.services.syntactic.interfaces import StringInterface
from data.services.syntactic.utils import check_bool
from data.services.syntactic.utils import model_text


class StringAnalyser(StringInterface, Thread):
    """contains services for StringInterface"""

    def __init__(self, df, document_id):
        self.df = df
        self.document_id = document_id
        Thread.__init__(self)

    def get_min_length(self):
        """indicator for min length"""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].fillna("").str.len().min()
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M102_17,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        return res

    def get_max_length(self):
        """indicator for max length"""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].fillna("").str.len().max()
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M103_18,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        return res

    def get_average_length(self):
        """indicator for average length"""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].fillna("").str.len().mean()
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M104_19,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        return res

    def number_of_words(self, s_t=" "):
        """indicator of number of words."""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].fillna("").str.split(s_t).apply(len).sum()
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M105_8,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        return res

    def frequency_table(self):
        """String type indicator."""
        df = self.df
        columns = df.columns
        res = []
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                bool_mask = df[i].apply(check_bool)
                df = df[~bool_mask]
                alpha_mask = df[i].fillna("").str.contains("[a-zA-Z]")
                df_alpha = df[alpha_mask]
                strings = df_alpha[i].tolist()
                res.append(strings)
            else:
                res.append("None")
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M105_20,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        return res

    def count_number_of_words(self, s=" "):
        """indicator of number of words."""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].fillna("").str.split(s).apply(len).sum()
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M105_8,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        return res

    def count_values(self):
        """String type indicator."""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                bool_mask = df[i].apply(check_bool)
                df = df[~bool_mask]
                alpha_mask = df[i].fillna("").str.contains("[a-zA-Z]")
                df_alpha = df[alpha_mask]
                res[columns.get_loc(i)] = df_alpha[i].count()
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M108_11,
            defaults={"result": {i: res[columns.get_loc(i)] for i in columns}},
        )
        return res

    def model_data_frequency(self):
        """model the data and count the number of occurrences and percentage for the models"""
        df = self.df
        columns = df.columns
        percentages = []
        occurrences = []
        data_model = []
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                modeled_df = df[i].fillna("").apply(model_text)
                percentages.append(modeled_df.value_counts(normalize=True) * 100)
                occurrences.append(modeled_df.value_counts())
                data_model.append(np.array(modeled_df.value_counts().axes))
            else:
                data_model.append("None")
                occurrences.append(0)
                percentages.append(0)

        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M107_10,
            defaults={"result": {i: data_model[columns.get_loc(i)] for i in columns}},
        )
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M106_9,
            defaults={
                "result": {
                    i: (occurrences[columns.get_loc(i)], percentages[columns.get_loc(i)])
                    for i in columns
                }
            },
        )

        return data_model, percentages, occurrences

    def get_columns_type(self):
        """Get an estimate of the column type"""
        _, data_matching_dict = BaseAbstract.syntactic_validation_with_data_dict()
        regexp_column_type, regexp_matching_dict = BaseAbstract.syntactic_validation_with_regexp()
        matched_res = []
        res_types = []
        for i in range(len(regexp_column_type)):
            res = []
            most_matched_reg = max(regexp_matching_dict[i], key=regexp_matching_dict[i].get)
            most_matched_data = max(data_matching_dict[i], key=data_matching_dict[i].get)
            if most_matched_reg == ("no-match", "no-match"):
                res.append(most_matched_data)
                res_types.append("datadict")
            else:
                res.append(most_matched_reg)
                res_types.append("regexp")
            matched_res.append(res)
        SemanticData.objects.update_or_create(
            document_id=self.document_id,
            defaults={"data": {i: res_types[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=COLUMN_TYPE,
            defaults={
                "result": {i: matched_res[self.df.columns.get_loc(i)] for i in self.df.columns}
            },
        )

    def link(self):
        """
        Define the links between columns of the type string by calculating the rate of
        similarity between these columns.
        For example two columns with identical values have a similarity score of 100%.
        """
        df = self.df
        columns = df.columns
        for col1 in columns:
            for col2 in columns[columns.get_loc(col1) + 1 :]:
                s = df[col1].apply(fuzz.token_set_ratio, s2=df[col2]).mean()
                if is_string_dtype(df[col1].dtypes) and is_string_dtype(df[col2].dtypes) and s > 80:
                    Link.objects.update_or_create(
                        document_id=self.document_id,
                        first_column=col1,
                        second_column=col2,
                        defaults={"relationship": str(s) + "% similarity score"},
                    )

    def run(self):
        self.get_min_length()
        self.get_max_length()
        self.get_average_length()
        self.frequency_table()
        self.count_number_of_words()
        self.count_values()
        self.model_data_frequency()
        # self.get_columns_type()
        AnalysisTrace.objects.update_or_create(
            document_id=self.document_id,
            analysis_type=STRING_ANALYSIS,
            defaults={"state": FINISHED_STATE},
        )
        self.link()
