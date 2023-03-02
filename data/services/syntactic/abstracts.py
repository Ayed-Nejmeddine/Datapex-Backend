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
from data.models.basic_models import SyntacticResult
from data.services.syntactic.interfaces import BaseInterface
from data.services.syntactic.utils import check_bool


class BaseAbstract(BaseInterface):
    """contains services for the BaseInterface"""

    def __init__(self, d_f, document_id):
        self.d_f = d_f
        self.document_id = document_id

    def number_null_values(self, inverse=False):
        """count the NULL values and the NOT NULL values"""
        d_f = self.d_f
        # Total number of values
        total = d_f.shape[0]
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=TOTAL,
            defaults={"result": {i: total for i in self.d_f.columns}},
        )
        res = pd.isnull(d_f).sum()
        rule = M100_3
        if inverse:
            res = d_f.count()
            rule = M101_4
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=rule,
            defaults={"result": {i: res[self.d_f.columns.get_loc(i)] for i in self.d_f.columns}},
        )
        return np.array(res)

    def count_distinct_values(self):
        """Indicator of the number of distinct values."""
        res = np.array(self.d_f.nunique())
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M102_5,
            defaults={"result": {i: res[self.d_f.columns.get_loc(i)] for i in self.d_f.columns}},
        )
        return res

    def count_unique_values(self):
        """Indicator of the number of unique values.
        Unique values are the values that exist only once."""
        d_f = self.d_f
        columns = d_f.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            res[columns.get_loc(i)] = len(d_f[i].drop_duplicates(keep=False))
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M103_6,
            defaults={"result": {i: res[self.d_f.columns.get_loc(i)] for i in self.d_f.columns}},
        )
        return res

    def count_different_values(self):
        """Indicator of the number of different values in each column."""
        d_f = self.d_f
        columns = d_f.columns
        res = []
        for col in columns:
            res.append(len(set(d_f[col])))
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M103_7,
            defaults={"result": {i: res[self.d_f.columns.get_loc(i)] for i in self.d_f.columns}},
        )
        return res

    def count_duplicated_values(self):
        """indicator of number of duplicated values."""
        res = self.count_distinct_values() - self.count_unique_values()
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M104_7,
            defaults={"result": {i: res[self.d_f.columns.get_loc(i)] for i in self.d_f.columns}},
        )
        return res

    def number_null_type_values(self, null="NULL"):
        """indicator of number of null type values."""
        d_f = self.d_f
        columns = d_f.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_bool_dtype(d_f[i].dtypes):
                res[columns.get_loc(i)] = d_f[i].str.count(null).sum()
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M112_15,
            defaults={"result": {i: res[self.d_f.columns.get_loc(i)] for i in self.d_f.columns}},
        )
        return res

    def count_boolean_type_values(self):
        """indicator of number of boolean type values"""
        d_f = self.d_f
        columns = d_f.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_bool_dtype(d_f[i].dtypes):
                res[columns.get_loc(i)] = d_f[i].count()
            elif is_string_dtype(d_f[i].dtypes):
                res[columns.get_loc(i)] = d_f[i].fillna("").apply(check_bool).sum()
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M111_14,
            defaults={"result": {i: res[self.d_f.columns.get_loc(i)] for i in self.d_f.columns}},
        )
        return res
