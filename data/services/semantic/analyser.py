from data.services.semantic.interfaces import SemanticInterface
from data.models.basic_models import SyntacticResult, SemanticResult
from data.models import MATCHED_EXPRESSIONS, DATA_TYPES
from data.services.syntactic.string import StringAnalyser
import numpy as np
from data.models import M101_1


class SemanticAnalyser(SemanticInterface):
    """ contains services for SemanticInterface """
    def __init__(self, df, document_id):
        super().__init__()
        self.df = df
        self.document_id = document_id

    def count_number_of_categories(self):
        """Count the number of the detected categories."""
        columns = self.df.columns
        res = np.zeros(len(columns), dtype=int)
        qs_reg = SyntacticResult.objects.get(document_id=self.document_id, rule=MATCHED_EXPRESSIONS)
        qs_data = SyntacticResult.objects.get(document_id=self.document_id, rule=DATA_TYPES)
        if not qs_reg and not qs_data:
            syntactic_analyser = StringAnalyser(self.df, self.document_id)
            syntactic_analyser.syntactic_validation_with_regexp()
            syntactic_analyser.syntactic_validation_with_data_dict()
        for i in qs_reg.result:
            res[columns.get_loc(i)] = len(set(qs_reg.result[i][0] + qs_data.result[i][0]))
        SemanticResult.objects.update_or_create(document_id=self.document_id, rule=M101_1,
                                                defaults={'result':{i: res[columns.get_loc(i)] for i in columns}})
