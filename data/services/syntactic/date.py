"""DateAnalyser"""
from threading import Thread

import numpy as np
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype
from pandas.api.types import is_string_dtype

from data.models import AFTER
from data.models import BEFORE
from data.models import DATE_ANALYSIS
from data.models import EQUALS
from data.models import FINISHED_STATE
from data.models import M110_13
from data.models import M112
from data.models import M113
from data.models import M114
from data.models import M115
from data.models import M116
from data.models import M117
from data.models import M118
from data.models import M119
from data.models import M120
from data.models import M121
from data.models import M122
from data.models.basic_models import AnalysisTrace
from data.models.basic_models import Link
from data.models.basic_models import SyntacticResult
from data.services.syntactic.interfaces import DateInterface
from data.services.syntactic.utils import check_format


class DateAnalyser(DateInterface, Thread):
    """contains services for DateInterface"""

    def __init__(self, df, document_id):
        self.df = df
        self.document_id = document_id
        Thread.__init__(self)

    def check_format_for_dataframe(self, rule, date_format):
        """For a given format, an array of booleans is returned where each value reflects the
        existence of a date according to this format in the corresponding column."""
        df = self.df
        columns = df.columns
        res = [0] * len(columns)
        for date_for in date_format:
            for i in columns:
                if is_string_dtype(df[i].dtypes):
                    res[columns.get_loc(i)] += (
                        df[i].fillna("").apply(check_format, date_format=date_for).sum()
                    )
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=rule,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        return res


    def count_values(self):
        """Datetime type indicator."""
        rule = M110_13
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(df[i].dtypes) or is_datetime64_any_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].apply(pd.to_datetime, errors="coerce").count()
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=rule,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        return res

    def link(self):
        """Define the links (either before , after or equals) between columns of the type date"""
        df = self.df
        columns = df.columns
        for col1 in columns:
            for col2 in columns[columns.get_loc(col1) + 1 :]:
                if (
                    is_string_dtype(df[col1].dtypes) or is_datetime64_any_dtype(df[col1].dtypes)
                ) and (
                    is_string_dtype(df[col2].dtypes) or is_datetime64_any_dtype(df[col2].dtypes)
                ):
                    first_col = df[col1].apply(pd.to_datetime, errors="coerce").tolist()
                    second_col = df[col2].apply(pd.to_datetime, errors="coerce").tolist()
                    equals = 0
                    before = 0
                    after = 0
                    for i in range(len(first_col)):
                        if first_col[i] < second_col[i]:
                            before += 1
                        elif first_col[i] > second_col[i]:
                            after += 1
                        elif first_col[i] == second_col[i]:
                            equals += 1
                    decision_val = max(before, after, equals) * 100 / len(first_col)
                    if decision_val > 50:
                        if decision_val == equals * 100 / len(first_col):
                            Link.objects.update_or_create(
                                document_id=self.document_id,
                                first_column=col1,
                                second_column=col2,
                                defaults={"relationship": str(decision_val) + "% " + EQUALS},
                            )
                        elif decision_val == before * 100 / len(first_col):
                            Link.objects.update_or_create(
                                document_id=self.document_id,
                                first_column=col1,
                                second_column=col2,
                                defaults={"relationship": str(decision_val) + "% " + BEFORE},
                            )
                        elif decision_val == after * 100 / len(first_col):
                            Link.objects.update_or_create(
                                document_id=self.document_id,
                                first_column=col1,
                                second_column=col2,
                                defaults={"relationship": str(decision_val) + "% " + AFTER},
                            )

    def run(self):
        self.count_values()
        self.check_format_for_dataframe(rule=M112, date_format=["%m/%d/%Y", "%m-%d-%Y"])
        self.check_format_for_dataframe(rule=M113, date_format=["%m/%d/%y", "%m-%d-%y"])
        self.check_format_for_dataframe(rule=M114, date_format=["%d/%b/%Y", "%d-%b-%Y", "%d %b %Y"])
        self.check_format_for_dataframe(rule=M115, date_format=["%d/%m/%Y", "%d-%m-%Y"])
        self.check_format_for_dataframe(rule=M116, date_format=["%Y/%m/%d", "%Y-%m-%d"])
        self.check_format_for_dataframe(rule=M117, date_format=["%H:%M", "%H:%M:%S"])
        self.check_format_for_dataframe(rule=M118, date_format=["%m/%d/%Y %H:%M"])
        self.check_format_for_dataframe(rule=M119, date_format=["%m/%d/%Y %H:%M:%S"])
        self.check_format_for_dataframe(rule=M120, date_format=["%B"])
        self.check_format_for_dataframe(rule=M121, date_format=["%A", "%a"])
        self.check_format_for_dataframe(rule=M122, date_format=["%B %d, %Y","%B %d %Y"])

        AnalysisTrace.objects.update_or_create(
            document_id=self.document_id,
            analysis_type=DATE_ANALYSIS,
            defaults={"state": FINISHED_STATE},
        )
        self.link()
