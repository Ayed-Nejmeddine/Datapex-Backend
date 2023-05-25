""" Abstract """
import numpy as np
import pandas as pd
from pandas.api.types import is_bool_dtype
from pandas.api.types import is_datetime64_any_dtype
from pandas.api.types import is_string_dtype

from data.models import DATA_TYPES
from data.models import M100_3
from data.models import M101_1
from data.models import M101_4
from data.models import M102_5
from data.models import M102_26
from data.models import M103_3
from data.models import M103_6
from data.models import M103_7
from data.models import M103_8
from data.models import M103_26
from data.models import M103_27
from data.models import M104_7
from data.models import M104_20
from data.models import M104_21
from data.models import M105_5
from data.models import M111_14
from data.models import M112_15
from data.models import M113_16
from data.models import M114_17
from data.models import M115_18
from data.models import M130_1
from data.models import M130_2
from data.models import M130_3
from data.models import MATCHED_EXPRESSIONS
from data.models import TOTAL
from data.models.basic_models import DataDict
from data.models.basic_models import RegularExp
from data.models.basic_models import SyntacticResult
from data.services.syntactic.interfaces import BaseInterface
from data.services.syntactic.utils import check_lower_case
from data.services.syntactic.utils import check_string_contains_bool
from data.services.syntactic.utils import get_data_dict
from data.services.syntactic.utils import get_regexp
from data.services.syntactic.utils import verify_MixCasse
from data.services.syntactic.utils import verify_Uppercase


class BaseAbstract(BaseInterface):
    """contains services for the BaseInterface"""

    def __init__(self, df, document_id):
        self.df = df
        self.document_id = document_id

    def count_null_values(self, inverse=False):
        """count the NULL values and the NOT NULL values"""
        df = self.df
        # Total number of values
        total = df.shape[0]
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=TOTAL,
            defaults={"result": {i: total for i in self.df.columns}},
        )
        res = pd.isnull(df).sum()
        rule = M100_3
        if inverse:
            res = df.count()
            rule = M101_4
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=rule,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        return np.array(res)

    def count_distinct_values(self):
        """Indicator of the number of distinct values."""
        res = np.array(self.df.nunique())
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M102_5,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        return res

    def count_unique_values(self):
        """Indicator of the number of unique values.
        Unique values are the values that exist only once."""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            res[columns.get_loc(i)] = len(df[i].drop_duplicates(keep=False))
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M103_6,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        return res

    def count_different_values(self):
        """Indicator of the number of different values in each column."""
        df = self.df
        columns = df.columns
        res = []
        for col in columns:
            res.append(len(set(df[col])))
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M103_7,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        return res

    def count_null_values_by_type(self, null=None):
        """indicator of number of null type values."""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if null:
                res[columns.get_loc(i)] = df[i].fillna("").str.count(null).sum()
            else:
                res[columns.get_loc(i)] = df[i].isnull().sum()
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M112_15,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        return res

    def count_duplicated_values(self):
        """indicator of number of duplicated values."""
        res = self.count_distinct_values() - self.count_unique_values()
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M104_7,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        return res

    def number_null_type_values(self, null="NULL"):
        """indicator of number of null type values."""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_bool_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].str.count(null).sum()
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M112_15,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        return res

    def count_boolean_type_values(self):
        """indicator of number of boolean type values"""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_bool_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].count()
            if is_string_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].apply(check_string_contains_bool).sum()

        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M111_14,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        return res

    def count_number_columns(self):
        """
        indicator of number of columns
        """
        df = self.df
        num_cols = df.shape[1]
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id, rule=M130_1, defaults={"result": num_cols}
        )
        return num_cols

    def values_length(self):
        """Indicator of length of each value"""
        df = self.df
        lengths = df.applymap(lambda x: len(str(x)) if pd.notnull(x) else None)
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M130_2,
            defaults={"result": {i: lengths[i] for i in self.df.columns}},
        )

    def count_init_CapCase_value(self):
        """Indicator of number of CapCase values"""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        is_capcase = df.applymap(lambda x: 1 if str(x)[0].isupper() else 0)
        for i in columns:
            res[columns.get_loc(i)] = is_capcase[i].sum()
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M130_3,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        return res

    def count_number_rows(self):
        """indicator of number of rows."""
        df = self.df
        res = len(df)
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id, rule=M113_16, defaults={"result": {"Rows": res}}
        )
        return res

    def data_type_value(self):
        """indicator of data type of the data values"""
        total = self.count_number_rows()
        result = []
        columns = self.df.columns
        for col in columns:
            df = self.df
            text_count = 0
            number_count = 0
            date_count = 0
            boolean_count = 0
            if is_string_dtype(df[col].dtypes) or is_datetime64_any_dtype(df[col].dtypes):
                date_mask = df[col].apply(pd.to_datetime, errors="coerce").notna()
                df_date = df[date_mask]
                date_count = df_date[col].count()
                df = df[~date_mask]
            if is_bool_dtype(df[col].dtypes):
                boolean_count = df[col].count()
            if is_string_dtype(df[col].dtypes) and df[col].notnull().any():
                boolean_count = df[col].apply(check_string_contains_bool).sum()
                bool_mask = df[col].apply(check_string_contains_bool)
                df = df[~bool_mask]
                alpha_mask = df[col].fillna("").str.contains("[a-zA-Z]")
                df_no_alpha = df[~alpha_mask]
                text_count = df[col].fillna("").count()
                number_count = df_no_alpha[col].apply(pd.to_numeric, errors="coerce").count()
            else:
                if df[col].dtype in ["float", "int"]:
                    number_count = df[col].fillna(0).apply(pd.to_numeric, errors="coerce").count()
            result.append(
                {
                    "string": round((text_count * 100) / total, 2),
                    "number": round((number_count * 100) / total, 2),
                    "boolean": round((boolean_count * 100) / total, 2),
                    "date": round((date_count * 100) / total, 2),
                }
            )

        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M114_17,
            defaults={"result": {i: result[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        return result

    def count_lowercase_values(self):
        """indicator of number of lowercase values"""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].fillna("").apply(check_lower_case).sum()
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M115_18,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        return res

    def count_number_of_values(self):
        """Indicator of the number of values in the dataset."""
        df = self.df
        rows = df.axes[0]
        cols = df.axes[1]
        res = len(rows) * len(cols)
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M103_8,
            defaults={"result": {"Size": res}},
        )
        return res

    def upper_case_values(self, s_t=" "):
        """This indicator function returns 1 if the value is in uppercase, and 0 otherwise."""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                nbr = df[i].fillna(s_t).apply(verify_Uppercase).sum()
                res[columns.get_loc(i)] = nbr
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M104_20,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        return res

    def mix_case_values(self, s_t=" "):
        """This indicator function returns 1 if the value is in uppercase, and 0 otherwise."""
        df = self.df
        columns = df.columns
        rowLength = len(df)
        res = np.zeros(len(columns), dtype=float)
        for i in columns:
            if is_string_dtype(df[i].dtypes) and not is_datetime64_any_dtype(df[i].dtypes):
                nbr = df[i].fillna(s_t).apply(verify_MixCasse).sum()
                res[columns.get_loc(i)] = round((nbr * 100) / rowLength, 2)
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M104_21,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )

        return res

    def _detected_types(self, matched_dict_percentages):
        """detect category, subcategory and percentage of the column"""
        detected_types = []
        column_detected_types = []

        for tuple_value in matched_dict_percentages:
            if tuple_value not in detected_types:
                cat_sub_val = {
                    "CATEGORY": tuple_value[0],
                    "SUBCATEGORY": tuple_value[1],
                    "POURCENTAGE": matched_dict_percentages[tuple_value],
                }
                column_detected_types.append(cat_sub_val)
                detected_types.append(tuple_value)
            else:
                column_detected_types[detected_types.index(tuple_value)][
                    "POURCENTAGE"
                ] += matched_dict_percentages[tuple_value]
        return column_detected_types

    def _detected_categories(self, column_detected_types):
        """detected categories in the column"""
        column_detected_category = {}
        for col_type in column_detected_types:
            if col_type["CATEGORY"] not in column_detected_category:
                column_detected_category[col_type["CATEGORY"]] = col_type["POURCENTAGE"]
            else:
                column_detected_category[col_type["CATEGORY"]] += col_type["POURCENTAGE"]
        return column_detected_category

    def _column_dominant_category(self, column_detected_category):
        """detect the dominant category in the column"""
        result_dict = {}
        for key in column_detected_category:
            if column_detected_category[key] == max(column_detected_category.values()):
                result_dict[key] = column_detected_category[key]
                break
        return result_dict

    def _column_dominant_subcategory(self, column_dominant_categories, column_detected_types):
        """detect the dominant subcategory in the column"""
        column_dominant_sub_categories = {}
        if column_dominant_categories:
            maxVal = 0
            first_key = next(iter(column_dominant_categories.keys()))
            for col_type in column_detected_types:
                if col_type["CATEGORY"] == first_key and col_type["POURCENTAGE"] > maxVal:
                    maxVal = col_type["POURCENTAGE"]
                    sub_cat = col_type["SUBCATEGORY"]
            column_dominant_sub_categories[sub_cat] = maxVal
            return column_dominant_sub_categories

        return "NON APPLICABLE"

    def _update_or_create_db(self, columns, rule, result):
        """updates or create a database row using the rule"""
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=rule,
            defaults={"result": {i: result[columns.get_loc(i)] for i in columns}},
        )

    def syntactic_validation_with_regexp(self):
        """Returns the number of categories and subcategories in each column"""
        df = self.df
        columns = df.columns
        expressions = RegularExp.objects.all().values_list("category", "subcategory", "expression")
        global_detected_types = []
        global_detected_categories = []
        global_dominant_categories = []
        global_dominant_subcategories = []
        for i in columns:
            df[i] = df[i].apply(lambda x: str(x).replace("Â°", "°"))
            data_serie = (
                df[i]
                .value_counts(dropna=False)
                .keys()
                .to_series()
                .apply(get_regexp, expressions=expressions)
            )
            data = data_serie.tolist()
            matched_dict = {cat_sub: data.count(cat_sub) for cat_sub in data}
            matched_dict_percentages = {
                key: round(int(matched_dict[key] * 100 / len(df[i])), 2) for key in matched_dict
            }
            column_detected_types = self._detected_types(matched_dict_percentages)
            global_detected_types.append(column_detected_types)
            column_detected_category = self._detected_categories(column_detected_types)
            global_detected_categories.append(column_detected_category)
            # the determination of the dominant category will be changed and we will consider the percentage of the dominant catgeory must be greater than 50%
            column_dominant_categories = self._column_dominant_category(column_detected_category)
            global_dominant_categories.append(column_dominant_categories)
            column_dominant_sub_categories = self._column_dominant_subcategory(
                column_dominant_categories, column_detected_types
            )
            global_dominant_subcategories.append(column_dominant_sub_categories)
        self._update_or_create_db(columns, MATCHED_EXPRESSIONS, global_detected_types)
        self._update_or_create_db(columns, M101_1, global_detected_categories)
        self._update_or_create_db(columns, M103_3, global_dominant_categories)
        self._update_or_create_db(columns, M105_5, global_dominant_subcategories)
        return (
            global_detected_types,
            global_detected_categories,
            global_dominant_categories,
            global_dominant_subcategories,
        )

    def syntactic_validation_with_data_dict(self):
        """
        Syntactically validate the data according to the data dictionary.
        res is an array of the number of syntactically valid data according to the data dictionary.
        invalid_res is an array of the number of syntactically invalid data according to the data dictionary.
        data_types will contain the data types of each column (exp: city, airport, firstname, etc...) and percentages will contain the percentages of
        the data_types in each column.
        """
        data_dict = DataDict.objects.all()
        df = self.df
        columns = df.columns
        #  TODO: Matching with the data dict takes a long time due to the size of the data_dict.  # pylint: disable=W0511

        global_detected_types = []
        global_detected_categories = []
        global_dominant_categories = []
        global_dominant_subcategories = []

        for i in columns:
            if is_string_dtype(df[i].dtypes):
                data_serie = (
                    df[i]
                    .value_counts(dropna=False)
                    .keys()
                    .to_series()
                    .apply(get_data_dict, data_dict=data_dict)
                )
                data = data_serie.tolist()
                matched_dict = {cat_sub: data.count(cat_sub) for cat_sub in data}
                matched_dict_percentages = {
                    key: round(int(matched_dict[key] * 100 / len(df[i])), 2) for key in matched_dict
                }
                column_detected_types = self._detected_types(matched_dict_percentages)
                global_detected_types.append(column_detected_types)
                column_detected_category = self._detected_categories(column_detected_types)
                global_detected_categories.append(column_detected_category)
                # the determination of the dominant category will be changed and we will consider the percentage of the dominant catgeory must be greater than 50%
                column_dominant_categories = self._column_dominant_category(
                    column_detected_category
                )
                global_dominant_categories.append(column_dominant_categories)
                column_dominant_sub_categories = self._column_dominant_subcategory(
                    column_dominant_categories, column_detected_types
                )
                global_dominant_subcategories.append(column_dominant_sub_categories)
            else:
                global_detected_types.append("NON APPLICABLE")
                global_detected_categories.append("NON APPLICABLE")
                global_dominant_categories.append("NON APPLICABLE")
                global_dominant_subcategories.append("NON APPLICABLE")

        # data types: detected categories and subcategories and their respectful percentages according to the data dictionary
        self._update_or_create_db(columns, DATA_TYPES, global_detected_types)
        # Detected categories and their respectful percentages according to the data dictionary
        self._update_or_create_db(columns, M103_26, global_detected_categories)
        # Dominant categories according to data dict
        self._update_or_create_db(columns, M102_26, global_dominant_categories)
        # Number of valid values according to the dominant Subcategory according to the data dictionary
        self._update_or_create_db(columns, M103_27, global_dominant_subcategories)
        return (
            global_detected_types,
            global_detected_categories,
            global_dominant_categories,
            global_dominant_subcategories,
        )
