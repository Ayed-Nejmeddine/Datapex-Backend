from data.services.semantic.interfaces import SemanticInterface
from data.models.basic_models import SyntacticResult, SemanticResult
from data.models import MATCHED_EXPRESSIONS, DATA_TYPES
from data.services.syntactic.string import StringAnalyser
import numpy as np
from data.models import M101_1, M102_2


class SemanticAnalyser(SemanticInterface):
    """ contains services for SemanticInterface """
    def __init__(self, df, document_id):
        super().__init__()
        self.df = df
        self.document_id = document_id

    def count_number_of_categories_and_subcategories(self):
        """Count the number of the detected categories and subcategories."""
        columns = self.df.columns
        res_cat = np.zeros(len(columns), dtype=int)
        res_subcat = np.zeros(len(columns), dtype=int)
        qs_reg = SyntacticResult.objects.get(document_id=self.document_id, rule=MATCHED_EXPRESSIONS)
        qs_data = SyntacticResult.objects.get(document_id=self.document_id, rule=DATA_TYPES)
        if not qs_reg and not qs_data:
            syntactic_analyser = StringAnalyser(self.df, self.document_id)
            syntactic_analyser.syntactic_validation_with_regexp()
            syntactic_analyser.syntactic_validation_with_data_dict()
        for i in qs_reg.result:
            res = qs_reg.result[i][0] + qs_data.result[i][0]
            categories = [cat[0] for cat in res]
            res_cat[columns.get_loc(i)] = len(set(categories))
            res_subcat[columns.get_loc(i)] = len(set(tuple(x) for x in res))
        SemanticResult.objects.update_or_create(document_id=self.document_id, rule=M101_1,
                                                defaults={'result':{i: res_cat[columns.get_loc(i)] for i in columns}})
        SemanticResult.objects.update_or_create(document_id=self.document_id, rule=M102_2,
                                                defaults={'result': {i: res_subcat[columns.get_loc(i)] for i in columns}})
