import pandas as pd
from data.services.syntactic.abstracts import BaseAbstract
from data.services.syntactic.string import StringAnalyser
from data.services.syntactic.number import NumberAnalyser
from data.services.syntactic.date import DateAnalyser
from threading import Thread
from data.models.basic_models import AnalysisTrace
from data.models import BASIC_ANALYSIS, STRING_ANALYSIS, NUMBER_ANALYSIS, DATE_ANALYSIS, FINISHED_STATE, RUNNING_STATE


class Analyser(BaseAbstract, Thread):

    def __init__(self, document):
        self.document_id = document.id
        with document.document_path.open('r') as f:
            df = pd.DataFrame(pd.read_csv(f))
            self.df = df.convert_dtypes()
        self.string_analyser = StringAnalyser(df, document.id)
        self.number_analyser = NumberAnalyser(df, document.id)
        self.date_analyser = DateAnalyser(df, document.id)
        Thread.__init__(self)

    def run(self):
        self.count_null_values(inverse=True)
        self.count_null_values()
        self.count_distinct_values()
        self.count_duplicated_values()
        self.count_unique_values()
        self.count_null_type_values()
        self.count_boolean_type_values()
        AnalysisTrace.objects.update_or_create(document_id=self.document_id, analysis_type=BASIC_ANALYSIS,
                                               defaults={'state': FINISHED_STATE})

        # start the thread for the string analysis
        AnalysisTrace.objects.update_or_create(document_id=self.document_id, analysis_type=STRING_ANALYSIS,
                                               defaults={'document_id': self.document_id, 'analysis_type': STRING_ANALYSIS, 'state': RUNNING_STATE})
        self.string_analyser.start()

        # start the thread for the number analysis
        AnalysisTrace.objects.update_or_create(document_id=self.document_id, analysis_type=NUMBER_ANALYSIS,
                                               defaults={'document_id': self.document_id, 'analysis_type': NUMBER_ANALYSIS, 'state': RUNNING_STATE})
        self.number_analyser.start()

        # start the thread for the date analysis
        AnalysisTrace.objects.update_or_create(document_id=self.document_id, analysis_type=DATE_ANALYSIS,
                                               defaults={'document_id': self.document_id, 'analysis_type': DATE_ANALYSIS, 'state': RUNNING_STATE})
        self.date_analyser.start()
