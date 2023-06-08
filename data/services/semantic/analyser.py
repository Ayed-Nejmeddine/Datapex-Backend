"""
    SemanticAnalyser
    """


from data.models import DATA_TYPES
from data.models import M101_1
from data.models import M102_25
from data.models import M102_26
from data.models import M103_3
from data.models import M103_5
from data.models import M103_26
from data.models import M103_27
from data.models import M103_30
from data.models import M103_31
from data.models import M104_5
from data.models import M104_6
from data.models import M104_26
from data.models import M104_27
from data.models import M104_28
from data.models import M105_5
from data.models import M113_16
from data.models import MATCHED_EXPRESSIONS
from data.models.basic_models import SemanticResult
from data.models.basic_models import SyntacticResult
from data.services.semantic.interfaces import SemanticInterface
from data.services.syntactic.abstracts import BaseAbstract


class SemanticAnalyser(SemanticInterface):
    """contains services for SemanticInterface"""

    def __init__(self, df, document_id):
        super().__init__()
        self.df = df
        self.document_id = document_id

    def count_number_of_categories_and_subcategories(self):
        """detected categories, dominant categories, dominant subcategories and their respectful percentages according to regexp and data_dict."""
        global_dominant_categories = {}
        global_dominant_sub_categories = {}
        global_categories = {}
        global_index_result = {}
        qs_reg = SyntacticResult.objects.get(
            document_id=self.document_id, rule=MATCHED_EXPRESSIONS
        )  # global_detected_types regexp {category: ,subcategory: ,sum: }
        M104_26_res = SyntacticResult.objects.get(
            document_id=self.document_id, rule=M104_26
        )  # profilage
        M104_27_res = SyntacticResult.objects.get(
            document_id=self.document_id, rule=M104_27
        )  # profilage
        M103_3_res = SyntacticResult.objects.get(
            document_id=self.document_id, rule=M103_3
        )  # dominant categories {domCat: 64}
        M105_5_res = SyntacticResult.objects.get(
            document_id=self.document_id, rule=M105_5
        )  # dominant subcategories {'first_name': {'no-match': 94.59},...}
        M101_1_res = SyntacticResult.objects.get(
            document_id=self.document_id, rule=M101_1
        )  # global_detected_categories regexp{'first_name': {'no-match': 94.59, 'BIC-BANKCODE': 5.41},...}
        qs_dict = SyntacticResult.objects.get(
            document_id=self.document_id, rule=DATA_TYPES
        )  # global_detected_types data dict{category: ,subcategory: ,sum: }
        M102_26_res = SyntacticResult.objects.get(
            document_id=self.document_id, rule=M102_26
        )  # profilage
        M103_27_res = SyntacticResult.objects.get(
            document_id=self.document_id, rule=M103_27
        )  # profilage
        M103_26_res = SyntacticResult.objects.get(
            document_id=self.document_id, rule=M103_26
        )  # global_detected_categories data dict{'first_name': {'no-match': 94.59, 'BIC-BANKCODE': 5.41},...}
        # if not qs_reg or not qs_dict:
        #     syntactic_analyser = BaseAbstract(self.df, self.document_id)
        #     syntactic_analyser.syntactic_validation_with_regexp()
        #     syntactic_analyser.syntactic_validation_with_data_dict()
        qs_total = {}
        for column in qs_reg.result:
            global_index_values = {}
            for index in M104_27_res.result[column]:
                global_index_values[index] = []
                global_index_values[index].append(M104_27_res.result[column][index])

            for index in M104_26_res.result[column]:
                global_index_values[index].append(M104_26_res.result[column][index])
            global_index_result[column] = global_index_values
            if not (
                qs_reg.result[column] == "NON APPLICABLE"
                or list(M103_3_res.result[column].keys()) == ["no-match"]
            ):
                qs_total[column] = qs_reg.result[column]
                global_categories[column] = M101_1_res.result[column]
                global_dominant_categories[column] = M103_3_res.result[column]
                global_dominant_sub_categories[column] = M105_5_res.result[column]
            else:
                qs_total[column] = qs_dict.result[column]
                global_categories[column] = M103_26_res.result[column]
                global_dominant_categories[column] = M102_26_res.result[column]
                global_dominant_sub_categories[column] = M103_27_res.result[column]
        # detected categories, subcategories using regex and data_dict
        SemanticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M103_5,
            defaults={"result": qs_total},
        )
        # detected categories using regex and data_dict
        SemanticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M102_25,
            defaults={"result": global_categories},
        )
        # dominant categories and their respectful percentages according to regex and data_dict
        SemanticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M103_30,
            defaults={"result": global_dominant_categories},
        )
        # detected categories using regex and data_dict
        SemanticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M104_28,
            defaults={"result": global_index_result},
        )
        # dominant subcategories and their respectful percentages according to regex and data_dict
        SemanticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M103_31,
            defaults={"result": global_dominant_sub_categories},
        )

    def count_validation_percentages(self):
        """Count the percentage of the semantically valid and invalid to the dominant category and subcategory according to regex and data_dict"""
        dom_cat_res = SemanticResult.objects.get(document_id=self.document_id, rule=M103_30)
        dom_sub_cat_res = SemanticResult.objects.get(document_id=self.document_id, rule=M103_31)
        rows = SyntacticResult.objects.get(document_id=self.document_id, rule=M113_16)
        number_rows = rows.result["Rows"]

        if not dom_cat_res and not dom_sub_cat_res:
            syntactic_analyser = BaseAbstract(self.df, self.document_id)
            syntactic_analyser.syntactic_validation_with_regexp()
            syntactic_analyser.syntactic_validation_with_data_dict()
        if not number_rows:
            syntactic_analyser = BaseAbstract(self.df, self.document_id)
            syntactic_analyser.count_number_rows()

        # convert the percentages to numbers
        dom_cat = {
            k: {
                list(dom_cat_res.result[k].keys())[0]: list(dom_cat_res.result[k].values())[0]
                * number_rows
                / 100
            }
            if dom_cat_res.result[k] != "NON APPLICABLE"
            else {"no-match": 0}
            for k in dom_cat_res.result
        }
        dom_sub_cat = {
            k: {
                list(dom_sub_cat_res.result[k].keys())[0]: round(
                    list(dom_sub_cat_res.result[k].values())[0] * number_rows / 100
                )
            }
            if dom_sub_cat_res.result[k] != "NON APPLICABLE"
            else {"no-match": 0}
            for k in dom_sub_cat_res.result
        }
        invalid_dom_cat = {
            k: {list(dom_cat[k].keys())[0]: number_rows - list(dom_cat[k].values())[0]}
            for k in dom_cat
        }
        invalid_dom_sub_cat = {
            k: {list(dom_sub_cat[k].keys())[0]: number_rows - list(dom_sub_cat[k].values())[0]}
            for k in dom_sub_cat
        }
        # Number of invalid values according to dominant category
        SemanticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M104_5,
            defaults={"result": invalid_dom_cat},
        )
        # Number of invalid values according to dominant subcategory
        SemanticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M104_6,
            defaults={"result": invalid_dom_sub_cat},
        )
