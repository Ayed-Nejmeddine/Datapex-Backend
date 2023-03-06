"""indicator_number_syntactic"""
from threading import Thread

import numpy as np
import pandas as pd

from data.models import EQUALS
from data.models import FINISHED_STATE
from data.models import GREATER_THAN
from data.models import LESS_THAN
from data.models import M102_20
from data.models import M103_20
from data.models import M103_21
from data.models import M104_22
from data.models import M105_23
from data.models import M109_12
from data.models import NUMBER_ANALYSIS
from data.models.basic_models import AnalysisTrace
from data.models.basic_models import Link
from data.models.basic_models import SyntacticResult
from data.services.syntactic.interfaces import NumberInterface


class NumberAnalyser(NumberInterface, Thread):
    """contains services for NumberInterface"""

    def __init__(self, df, document_id):
        self.df = df
        self.document_id = document_id
        Thread.__init__(self)

    def compute_min_value(self):
        """indicator for min value."""
        mask = self.df.applymap(type) != bool
        res = self.df.where(mask, self.df.replace({True: "TRUE", False: "FALSE"}))
        res = res.apply(pd.to_numeric, errors="coerce").min()
        res = res.fillna("non-applicable")
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M102_20,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        return np.array(res)

    def compute_max_value(self):
        """indicator for max value."""
        mask = self.df.applymap(type) != bool
        res = self.df.where(mask, self.df.replace({True: "TRUE", False: "FALSE"}))
        res = res.apply(pd.to_numeric, errors="coerce").max()
        res = res.fillna("non-applicable")
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M103_20,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        return np.array(res)

    def compute_average_value(self):
        """indicator for average value."""
        mask = self.df.applymap(type) != bool
        res = self.df.where(mask, self.df.replace({True: "TRUE", False: "FALSE"}))
        res = res.apply(pd.to_numeric, errors="coerce").mean()
        res = res.fillna("non-applicable")
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M103_21,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        return np.array(res)

    def compute_mode_value(self):
        """indicator for mode value."""
        mask = self.df.applymap(type) != bool
        res = self.df.where(mask, self.df.replace({True: "TRUE", False: "FALSE"}))
        df = res.apply(pd.to_numeric, errors="coerce")
        df = df.replace(np.nan, "non-applicable", regex=True)
        res = df.mode().to_numpy()[0]
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M104_22,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        return np.array(res)

    def compute_median_value(self):
        """indicator for median value."""
        mask = self.df.applymap(type) != bool
        res = self.df.where(mask, self.df.replace({True: "True", False: "False"}))
        res = res.apply(pd.to_numeric, errors="coerce").median()
        res = res.fillna("non-applicable")
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M105_23,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        return np.array(res)

    def count_values(self):
        """indicator of Number of values of the NUMBER TYPE."""
        mask = self.df.applymap(type) != bool
        res = self.df.where(mask, self.df.replace({True: "True", False: "False"}))
        res = res.apply(pd.to_numeric, errors="coerce").count()
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M109_12,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        return np.array(res)

    def link(self):
        """Define the links (either greater than , less than or equals) between columns of the type numeric"""
        df = self.df
        df = df.apply(pd.to_numeric, errors="coerce")
        columns = df.columns
        for col1 in columns:
            for col2 in columns[columns.get_loc(col1) + 1 :]:
                if (df[col1] == df[col2]).all():
                    Link.objects.update_or_create(
                        document_id=self.document_id,
                        first_column=col1,
                        second_column=col2,
                        defaults={"relationship": EQUALS},
                    )
                elif (df[col1] <= df[col2]).all():
                    Link.objects.update_or_create(
                        document_id=self.document_id,
                        first_column=col1,
                        second_column=col2,
                        defaults={"relationship": LESS_THAN},
                    )
                elif (df[col1] >= df[col2]).all():
                    Link.objects.update_or_create(
                        document_id=self.document_id,
                        first_column=col1,
                        second_column=col2,
                        defaults={"relationship": GREATER_THAN},
                    )

    def run(self):
        self.compute_min_value()
        self.compute_max_value()
        self.compute_average_value()
        self.compute_mode_value()
        self.compute_median_value()
        self.count_values()
        AnalysisTrace.objects.update_or_create(
            document_id=self.document_id,
            analysis_type=NUMBER_ANALYSIS,
            defaults={"state": FINISHED_STATE},
        )
        self.link()
