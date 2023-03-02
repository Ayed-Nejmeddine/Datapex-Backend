"""StringAnalyser"""
from threading import Thread

import numpy as np
from fuzzywuzzy import fuzz
from pandas.api.types import is_string_dtype

from data.models import COLUMN_TYPE
from data.models import DATA_TYPES
from data.models import FINISHED_STATE
from data.models import M102_17
from data.models import M102_25
from data.models import M102_26
from data.models import M103_18
from data.models import M103_25
from data.models import M103_26
from data.models import M104_19
from data.models import M105_8
from data.models import M106_9
from data.models import M107_10
from data.models import M108_11
from data.models import MATCHED_EXPRESSIONS
from data.models import STRING_ANALYSIS
from data.models.basic_models import AnalysisTrace
from data.models.basic_models import DataDict
from data.models.basic_models import Link
from data.models.basic_models import RegularExp
from data.models.basic_models import SemanticData
from data.models.basic_models import SyntacticResult
from data.services.syntactic.interfaces import StringInterface
from data.services.syntactic.utils import check_bool
from data.services.syntactic.utils import get_data_dict
from data.services.syntactic.utils import get_regexp
from data.services.syntactic.utils import model_text


class StringAnalyser(StringInterface, Thread):
    """contains services for StringInterface"""

    def __init__(self, d_f, document_id):
        self.d_f = d_f
        self.document_id = document_id
        Thread.__init__(self)

    def get_min_length(self):
        """indicator for min length"""
        d_f = self.d_f
        columns = d_f.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(d_f[i].dtypes):
                res[columns.get_loc(i)] = d_f[i].fillna("").str.len().min()
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M102_17,
            defaults={"result": {i: res[self.d_f.columns.get_loc(i)] for i in self.d_f.columns}},
        )
        return res

    def get_max_length(self):
        """indicator for max length"""
        d_f = self.d_f
        columns = d_f.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(d_f[i].dtypes):
                res[columns.get_loc(i)] = d_f[i].fillna("").str.len().max()
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M103_18,
            defaults={"result": {i: res[self.d_f.columns.get_loc(i)] for i in self.d_f.columns}},
        )
        return res

    def get_average_length(self):
        """indicator for average length"""
        d_f = self.d_f
        columns = d_f.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(d_f[i].dtypes):
                res[columns.get_loc(i)] = d_f[i].fillna("").str.len().mean()
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M104_19,
            defaults={"result": {i: res[self.d_f.columns.get_loc(i)] for i in self.d_f.columns}},
        )
        return res

    def number_of_words(self, s_t=" "):
        """indicator of number of words."""
        d_f = self.d_f
        columns = d_f.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(d_f[i].dtypes):
                res[columns.get_loc(i)] = d_f[i].fillna("").str.split(s_t).apply(len).sum()
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M105_8,
            defaults={"result": {i: res[self.d_f.columns.get_loc(i)] for i in self.d_f.columns}},
        )
        return res

    def count_values(self):
        """String type indicator."""
        d_f = self.d_f
        columns = d_f.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(d_f[i].dtypes):
                bool_mask = d_f[i].apply(check_bool)
                d_f = d_f[~bool_mask]
                alpha_mask = d_f[i].fillna("").str.contains("[a-zA-Z]")
                d_f_alpha = d_f[alpha_mask]
                res[columns.get_loc(i)] = d_f_alpha[i].count()
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M108_11,
            defaults={"result": {i: res[self.d_f.columns.get_loc(i)] for i in self.d_f.columns}},
        )
        return res

    def model_data_frequency(self):
        """model the data and count the number of occurrences and percentage for the models"""
        d_f = self.d_f
        columns = d_f.columns
        percentages = []
        occurrences = []
        data_model = []
        for i in columns:
            if is_string_dtype(d_f[i].dtypes):
                modeled_df = d_f[i].fillna("").apply(model_text)
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

    def syntactic_validation_with_regexp(self):
        """
        Syntaxically validate the data according
        to the regular expressions in the model RegularExp.
        res will be an array of the number of syntactically
        valid data according to the regular expressions.
        invalid_res will be an array of the number of
        syntactically invalid data according to the regular
        expressions.
        """
        d_f = self.d_f
        columns = d_f.columns
        invalid_res = np.full(len(columns), np.array(d_f.shape[0]))
        matched_expressions = []
        percentages = []
        column_type = []
        total_dict = []
        for i in columns:
            if is_string_dtype(d_f[i].dtypes):
                reg_exp = (
                    d_f[i]
                    .value_counts(dropna=False)
                    .keys()
                    .to_series()
                    .apply(get_regexp, expressions=RegularExp.objects.all().values("expression"))
                )
                column_type.append(reg_exp)
                invalid_res[columns.get_loc(i)] = (
                    d_f[i].value_counts(dropna=False)[reg_exp.isna()].sum()
                )
                r_t = reg_exp.apply(lambda x: ("no-match", "no-match") if x is None else x)
                matched_dict = {}
                percentage = d_f[i].value_counts(dropna=False, normalize=True) * 100
                for j in r_t:
                    if j in matched_dict:
                        matched_dict[j] += percentage[matched_dict[j]]
                    else:
                        matched_dict[j] = percentage[matched_dict[j]]
                matched_expressions.append(matched_dict.keys())
                percentages.append(matched_dict.values())
                total_dict.append(matched_dict)
            else:
                matched_expressions.append(["non-applicable"])
                percentages.append([0])
                column_type.append([])
                total_dict.append({})
        res = np.array(d_f.shape[0]) - invalid_res
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M102_25,
            defaults={"result": {i: res[self.d_f.columns.get_loc(i)] for i in self.d_f.columns}},
        )
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=MATCHED_EXPRESSIONS,
            defaults={
                "result": {
                    i: (matched_expressions[columns.get_loc(i)], percentages[columns.get_loc(i)])
                    for i in columns
                }
            },
        )
        # the number of syntactically invalid data according to the regular expressions
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M103_25,
            defaults={
                "result": {i: invalid_res[self.d_f.columns.get_loc(i)] for i in self.d_f.columns}
            },
        )
        return column_type, total_dict

    def syntactic_validation_with_data_dict(self):
        """
        Syntactically validate the data
        according to the data dictionary.
        res is an array of the number of
        syntactically valid data according
        to the data dictionary.
        invalid_res is an array of the number
        of syntactically invalid data according
        to the data dictionary.
        data_types will contain the data types of each
        column (exp: city, airport, firstname, etc...)
        and percentages will contain the percentages
        of the data_types in each column.
        """
        d_f = self.d_f
        columns = d_f.columns
        invalid_res = np.full(len(columns), np.array(d_f.shape[0]))
        # TODO: Matching with the data dict takes a long time due to the size of the data_dict.
        # pylint: disable=W0511 # noqa: E501
        data_types = []
        percentages = []
        column_type = []
        total_dict = []
        for i in columns:
            if is_string_dtype(d_f[i].dtypes):
                d_t = (
                    d_f[i]
                    .value_counts(dropna=False)
                    .to_series()
                    .apply(get_data_dict, data_dict=DataDict.objects.all())
                )
                column_type.append(d_t)
                matched_res = d_t.apply(lambda x: ("no-match", "no-match") if x is None else x)
                matched_dict = {}
                percentage = d_f[i].value_counts(dropna=False, normalize=True) * 100
                for j in matched_res:
                    if j in matched_dict:
                        matched_res[j] += percentage[matched_dict[j]]
                    else:
                        matched_res[j] = percentage[matched_dict[j]]

                data_types.append(matched_dict)
                percentages.append(matched_dict.values())
                total_dict.append(matched_dict)
                invalid_res[columns.get_loc(i)] = (
                    d_f[i].value_counts(dropna=False)[d_t.isna()].sum()
                )
            else:
                data_types.append(["non-applicable"])
                percentages.append([0])
                column_type.append([])
                total_dict.append({})
        res = np.array(d_f.shape[0]) - invalid_res
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M102_26,
            defaults={"result": {i: res[self.d_f.columns.get_loc(i)] for i in self.d_f.columns}},
        )
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=DATA_TYPES,
            defaults={
                "result": {
                    i: (data_types[columns.get_loc(i)], percentages[columns.get_loc(i)])
                    for i in columns
                }
            },
        )
        # number of syntactically invalid data according to the data dictionary
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M103_26,
            defaults={
                "result": {i: invalid_res[self.d_f.columns.get_loc(i)] for i in self.d_f.columns}
            },
        )
        return column_type, total_dict

    def get_columns_type(self):
        """Get an estimate of the column type"""
        data_matching_dict = self.syntactic_validation_with_data_dict()[1]
        regexp_column_type, regexp_matching_dict = self.syntactic_validation_with_regexp()
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
            defaults={
                "data": {i: res_types[self.d_f.columns.get_loc(i)] for i in self.d_f.columns}
            },
        )
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=COLUMN_TYPE,
            defaults={
                "result": {i: matched_res[self.d_f.columns.get_loc(i)] for i in self.d_f.columns}
            },
        )

    def link(self):
        """
        Define the links between columns of the type
        string by calculating the rate of similarity
        between these columns.
        For example two columns with identical values
        have a similarity score of 100%.
        """
        d_f = self.d_f
        columns = d_f.columns
        for col1 in columns:
            for col2 in columns[columns.get_loc(col1) + 1 :]:
                s_t = d_f[col1].apply(fuzz.token_set_ratio, s2=d_f[col2]).mean()
                if (
                    is_string_dtype(d_f[col1].dtypes)
                    and is_string_dtype(d_f[col2].dtypes)
                    and s_t > 80
                ):
                    Link.objects.update_or_create(
                        document_id=self.document_id,
                        first_column=col1,
                        second_column=col2,
                        defaults={"relationship": str(s_t) + "% similarity score"},
                    )

    def run(self):
        self.get_min_length()
        self.get_max_length()
        self.get_average_length()
        self.count_number_of_words()
        self.count_values()
        self.model_data_frequency()
        self.get_columns_type()
        AnalysisTrace.objects.update_or_create(
            document_id=self.document_id,
            analysis_type=STRING_ANALYSIS,
            defaults={"state": FINISHED_STATE},
        )
        self.link()
