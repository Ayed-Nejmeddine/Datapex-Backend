""" Abstract """
import numpy as np
import pandas as pd
from pandas.api.types import is_bool_dtype
from pandas.api.types import is_datetime64_any_dtype
from pandas.api.types import is_string_dtype

from data.models import M100_3
from data.models import M101_4
from data.models import M102_5
from data.models import M103_6
from data.models import M103_7
from data.models import M104_7
from data.models import M111_14
from data.models import M112_15
from data.models import M113_16
from data.models import M114_17
from data.models import M115_18
from data.models import TOTAL
from data.models import M130_1
from data.models import M130_2
from data.models import M130_3

from data.models.basic_models import SyntacticResult
from data.services.syntactic.interfaces import BaseInterface
from data.services.syntactic.utils import check_lower_case
from data.services.syntactic.utils import check_string_contains_bool


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
        df=self.df
        num_cols=df.shape[1]
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M130_1,
            defaults={"result": num_cols}
        )
        return num_cols

    def values_length(self):
        """Indicator of length of each value
        """
        df=self.df
        lengths = df.applymap(lambda x: len(str(x)) if pd.notnull(x) else None)
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M130_2,
            defaults={"result": {i: lengths[i] for i in self.df.columns}},
        )


    def count_init_CapCase_value(self):
        """Indicator of number of CapCase values
        """
        df=self.df
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
        return(res)
            

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
        mask = self.df.applymap(type) != bool
        res = self.df.where(mask, self.df.replace({True: "True", False: "False"}))
        columns = res.columns
        for col in columns:
            text_count = 0
            number_count = 0
            date_count = 0
            boolean_count = 0
            if is_string_dtype(res[col].dtypes) or is_datetime64_any_dtype(res[col].dtypes):
                date_count = res[col].apply(pd.to_datetime, errors="coerce").count()
            if is_bool_dtype(res[col].dtypes):
                boolean_count = res[col].count()
            if is_string_dtype(res[col].dtypes):
                boolean_count = res[col].apply(check_string_contains_bool).sum()
                bool_mask = res[col].apply(check_string_contains_bool)
                self.df = res[~bool_mask]
                alpha_mask = self.df[col].fillna("").str.contains("[a-zA-Z]")
                df_alpha = self.df[alpha_mask]
                df_no_alpha = self.df[~alpha_mask]
                text_count = df_alpha[col].count()
                number_count = df_no_alpha[col].apply(pd.to_numeric, errors="coerce").count()
            else:
                number_count = res[col].apply(pd.to_numeric, errors="coerce").count()
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
        total = self.count_number_rows()
        columns = df.columns
        res = np.zeros(len(columns), dtype=float)
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = round(
                    (df[i].fillna("").apply(check_lower_case).sum() * 100) / total, 2
                )
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M115_18,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        return res
