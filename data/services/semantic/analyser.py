"""
    SemanticAnalyser
    """


from data.models import M101_1
from data.models import M102_2
from data.models import M103_3
from data.models import M104_4
from data.models import M105_5
from data.models import M106_6
from data.models import MATCHED_EXPRESSIONS
from data.models.basic_models import SemanticResult
from data.models.basic_models import SyntacticResult
from data.services.semantic.interfaces import SemanticInterface
from data.services.syntactic.string import StringAnalyser


class SemanticAnalyser(SemanticInterface):
    """contains services for SemanticInterface"""

    def __init__(self, df, document_id):
        super().__init__()
        self.df = df
        self.document_id = document_id

    def count_number_of_categories_and_subcategories(self):
        """Count the number of the detected categories and subcategories."""

        qs_reg = SyntacticResult.objects.get(document_id=self.document_id, rule=MATCHED_EXPRESSIONS)
        M101_res = SyntacticResult.objects.get(document_id=self.document_id, rule=M101_1)
        M102_res = SyntacticResult.objects.get(document_id=self.document_id, rule=M102_2)

        if not qs_reg and not M101_res and not M102_res:
            syntactic_analyser = StringAnalyser(self.df, self.document_id)
            syntactic_analyser.syntactic_validation_with_regexp()

        SemanticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=MATCHED_EXPRESSIONS,
            defaults={"result": qs_reg.result},
        )
        SemanticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M101_1,
            defaults={"result": M101_res.result},
        )

        SemanticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M102_2,
            defaults={"result": M102_res.result},
        )

    def count_validation_percentages(self):
        """Count the percentage of the semantically valid and invalid to the dominant category and subcategory"""

        M103_res = SyntacticResult.objects.get(document_id=self.document_id, rule=M103_3)
        M104_res = SyntacticResult.objects.get(document_id=self.document_id, rule=M104_4)
        M105_res = SyntacticResult.objects.get(document_id=self.document_id, rule=M105_5)
        M106_res = SyntacticResult.objects.get(document_id=self.document_id, rule=M106_6)
        if not M103_res and not M104_res and not M105_res and not M106_res:
            syntactic_analyser = StringAnalyser(self.df, self.document_id)
            syntactic_analyser.syntactic_validation_with_regexp()

        SemanticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M103_3,
            defaults={"result": M103_res.result},
        )

        SemanticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M104_4,
            defaults={"result": M104_res.result},
        )

        SemanticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M105_5,
            defaults={"result": M105_res.result},
        )

        SemanticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M106_6,
            defaults={"result": M106_res.result},
        )
