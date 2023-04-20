"""indicator_number_syntactic"""
from threading import Thread

import numpy as np
import pandas as pd
from pandas.api.types import is_bool_dtype
from pandas.api.types import is_string_dtype
from data.models import FINISHED_STATE
from data.models import M111_12
from data.models import BOOLEAN_ANALYSIS
from data.models.basic_models import AnalysisTrace
from data.models.basic_models import SyntacticResult
from data.services.syntactic.interfaces import BooleanInterface


class BooleanAnalyser(BooleanInterface, Thread):
    """contains services for BooleanInterface"""

    def __init__(self, df, document_id):
        self.df = df
        self.document_id = document_id
        Thread.__init__(self)

    def count_boolean_value(self):
        """indicator of number of boolean type values"""
        df = self.df
        columns = df.columns
        res=[]
        for i in columns:
            count_true=0
            count_false=0
            if is_bool_dtype(df[i].dtypes):
                value_counts = df[i].value_counts()
                if True in value_counts.index:
                    count_true = value_counts[True]
                if False in value_counts.index:
                    count_false = value_counts[False]
            if is_string_dtype(df[i].dtypes):
                true_values = df[i].apply(lambda x: str(x).lower() in ['true'])
                count_true=true_values.sum()
                false_values = df[i].apply(lambda x: str(x).lower() in ['false'])
                count_false=false_values.sum()
            res.append(
                {
                    "true": count_true,
                    "false": count_false
                }
            )
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M111_12,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        
        return res

    def run(self):
        self.count_boolean_value()
        AnalysisTrace.objects.update_or_create(
            document_id=self.document_id,
            analysis_type=BOOLEAN_ANALYSIS,
            defaults={"state": FINISHED_STATE},
        )