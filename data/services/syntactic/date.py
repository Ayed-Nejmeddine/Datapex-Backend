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
from data.models.basic_models import AnalysisTrace
from data.models.basic_models import Link
from data.models.basic_models import SyntacticResult
from data.services.syntactic.interfaces import DateInterface
from data.services.syntactic.utils import check_format


class DateAnalyser(DateInterface, Thread):
    """contains services for DateInterface"""

    def __init__(self, d_f, document_id):
        self.d_f = d_f
        self.document_id = document_id
        Thread.__init__(self)

    def check_format_dataframe(self, rule, date_format):
        """For a given format, an array of booleans is returned where each value reflects the
        existence of a date according to this format in the corresponding column."""
        d_f = self.d_f
        columns = d_f.columns
        res = [0] * len(columns)
        for date_for in date_format:
            for i in columns:
                if is_string_dtype(d_f[i].dtypes):
                    res[columns.get_loc(i)] += (
                        d_f[i].fillna("").apply(check_format, date_format=date_for).sum()
                    )

        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=rule,
            defaults={"result": {i: res[self.d_f.columns.get_loc(i)] for i in self.d_f.columns}},
        )
        return res

    def count_values(self):
        """Datetime type indicator."""
        rule = M110_13
        d_f = self.d_f
        columns = d_f.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(d_f[i].dtypes) or is_datetime64_any_dtype(d_f[i].dtypes):
                res[columns.get_loc(i)] = d_f[i].apply(pd.to_datetime, errors="coerce").count()
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=rule,
            defaults={"result": {i: res[self.d_f.columns.get_loc(i)] for i in self.d_f.columns}},
        )
        return res

    def link(self):
        """Define the links (either before , after or equals) between columns of the type date"""
        d_f = self.d_f
        columns = d_f.columns
        for col1 in columns:
            for col2 in columns[columns.get_loc(col1) + 1 :]:
                if (
                    is_string_dtype(d_f[col1].dtypes) or is_datetime64_any_dtype(d_f[col1].dtypes)
                ) and (
                    is_string_dtype(d_f[col2].dtypes) or is_datetime64_any_dtype(d_f[col2].dtypes)
                ):
                    first_col = d_f[col1].apply(pd.to_datetime, errors="coerce")
                    second_col = d_f[col2].apply(pd.to_datetime, errors="coerce")
                    if (first_col == second_col).all():
                        Link.objects.update_or_create(
                            document_id=self.document_id,
                            first_column=col1,
                            second_column=col2,
                            defaults={"relationship": EQUALS},
                        )
                    elif (first_col <= second_col).all():
                        Link.objects.update_or_create(
                            document_id=self.document_id,
                            first_column=col1,
                            second_column=col2,
                            defaults={"relationship": BEFORE},
                        )
                    elif (first_col >= second_col).all():
                        Link.objects.update_or_create(
                            document_id=self.document_id,
                            first_column=col1,
                            second_column=col2,
                            defaults={"relationship": AFTER},
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
        AnalysisTrace.objects.update_or_create(
            document_id=self.document_id,
            analysis_type=DATE_ANALYSIS,
            defaults={"state": FINISHED_STATE},
        )
        self.link()
