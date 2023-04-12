""" Abstract """
import numpy as np
import pandas as pd
from pandas.api.types import is_bool_dtype
from pandas.api.types import is_string_dtype

from data.models import M100_3
from data.models import M101_4
from data.models import M102_5
from data.models import M103_6
from data.models import M103_7
from data.models import M104_7
from data.models import M111_14
from data.models import M112_15
from data.models import TOTAL
from data.models import M130_1
from data.models import M130_2
from data.models import M130_3

from data.models.basic_models import SyntacticResult
from data.services.syntactic.interfaces import BaseInterface
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
            