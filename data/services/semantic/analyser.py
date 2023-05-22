from data.services.semantic.interfaces import SemanticInterface
from data.models.basic_models import SyntacticResult, SemanticResult, SemanticData
from data.models import MATCHED_EXPRESSIONS, DATA_TYPES, COLUMN_TYPE
from data.services.syntactic.string import StringAnalyser
import numpy as np
from data.models import M101_1, M102_2, M103_3, M104_4, M105_5, M106_6


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

    def count_validation_percentages(self):
        """ Count the percentage of the semantically valid and invalid to the dominant category and subcategory"""
        qs = SyntacticResult.objects.get(document_id=self.document_id, rule=COLUMN_TYPE)
        data_type = SemanticData.objects.get(document_id=self.document_id)
        nbr_valid_cat = []
        nbr_valid_subcat = []
        for i in qs.result:
            subcat = qs.result[i][0]
            if data_type.data[i] == 'datadict':
                qs_res = SyntacticResult.objects.get(document_id=self.document_id, rule=DATA_TYPES)
            else:
                qs_res = SyntacticResult.objects.get(document_id=self.document_id, rule=MATCHED_EXPRESSIONS)
            res_cat = 0
            for j in qs_res.result[i][0]:
                if j[0] == qs.result[i][0][0]:
                    res_cat += qs_res.result[i][1][qs_res.result[i][0].index(j)]
            nbr_valid_cat.append(res_cat)
            nbr_valid_subcat.append(qs_res.result[i][1][qs_res.result[i][0].index(subcat)])
        SemanticResult.objects.update_or_create(document_id=self.document_id, rule=M103_3,
                                                defaults={'result': {i: nbr_valid_cat[self.df.columns.get_loc(i)] for i in self.df.columns}})
        SemanticResult.objects.update_or_create(document_id=self.document_id, rule=M105_5,
                                                defaults={
                                                    'result': {i: nbr_valid_subcat[self.df.columns.get_loc(i)] for i in
                                                               self.df.columns}})

        nbr_invalid_cat = [100 - num for num in nbr_valid_cat]
        nbr_invalid_subcat = [100 - num for num in nbr_valid_subcat]
        SemanticResult.objects.update_or_create(document_id=self.document_id, rule=M104_4,
                                                defaults={'result': {i: nbr_invalid_cat[self.df.columns.get_loc(i)] for i in self.df.columns}})
        SemanticResult.objects.update_or_create(document_id=self.document_id, rule=M106_6,
                                                defaults={
                                                    'result': {i: nbr_invalid_subcat[self.df.columns.get_loc(i)] for i in
                                                               self.df.columns}})
