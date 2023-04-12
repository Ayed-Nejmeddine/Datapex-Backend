"""BaseAbstract Analyser."""
from threading import Thread

import pandas as pd

from data.models import BASIC_ANALYSIS
from data.models import DATE_ANALYSIS
from data.models import FINISHED_STATE
from data.models import NUMBER_ANALYSIS
from data.models import RUNNING_STATE
from data.models import STRING_ANALYSIS
from data.models.basic_models import AnalysisTrace
from data.services.syntactic.abstracts import BaseAbstract
from data.services.syntactic.date import DateAnalyser
from data.services.syntactic.number import NumberAnalyser
from data.services.syntactic.string import StringAnalyser


class Analyser(BaseAbstract, Thread):
    """BaseAbstract Analyser"""

    def __init__(self, document):
        super().__init__(self, document)
        self.document_id = document.id
        with document.document_path.open("r") as f:
            df = pd.DataFrame(pd.read_csv(f, sep=";"))
            self.df = df.convert_dtypes()
        document.num_row, document.num_col = df.shape
        document.save()
        columns = self.df.columns
        num_col = []
        date_col = []
        string_col = []
        for i in columns:
            if pd.to_numeric(df[i], errors="coerce").any():
                num_col.append(i)
            elif df[i].apply(pd.to_datetime, errors="coerce").count() > 0:
                date_col.append(i)
            else:
                string_col.append(i)
        self.string_analyser = StringAnalyser(df[string_col], document.id)
        self.number_analyser = NumberAnalyser(df[num_col], document.id)
        self.date_analyser = DateAnalyser(df[date_col], document.id)
        Thread.__init__(self)

    def run(self):
        self.count_null_values(inverse=True)
        self.count_null_values()
        self.count_distinct_values()
        self.count_duplicated_values()
        self.count_unique_values()
        self.count_null_type_values()
        self.count_boolean_type_values()
        self.count_number_rows()
        self.data_type_value()
        self.count_lowercase_values()
        self.mix_case_values()
        self.upper_case_values()
        self.count_number_of_values()
        AnalysisTrace.objects.update_or_create(
            document_id=self.document_id,
            analysis_type=BASIC_ANALYSIS,
            defaults={"state": FINISHED_STATE},
        )

        # start the thread for the string analysis
        AnalysisTrace.objects.update_or_create(
            document_id=self.document_id,
            analysis_type=STRING_ANALYSIS,
            defaults={
                "document_id": self.document_id,
                "analysis_type": STRING_ANALYSIS,
                "state": RUNNING_STATE,
            },
        )
        self.string_analyser.start()

        # start the thread for the number analysis
        AnalysisTrace.objects.update_or_create(
            document_id=self.document_id,
            analysis_type=NUMBER_ANALYSIS,
            defaults={
                "document_id": self.document_id,
                "analysis_type": NUMBER_ANALYSIS,
                "state": RUNNING_STATE,
            },
        )
        self.number_analyser.start()

        # start the thread for the date analysis
        AnalysisTrace.objects.update_or_create(
            document_id=self.document_id,
            analysis_type=DATE_ANALYSIS,
            defaults={
                "document_id": self.document_id,
                "analysis_type": DATE_ANALYSIS,
                "state": RUNNING_STATE,
            },
        )
        self.date_analyser.start()
