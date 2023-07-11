"""
    Profilage
"""
import ast

from data.models import M100_3
from data.models import M100_4
from data.models import M100_5
from data.models import M100_6
from data.models import M104_28
from data.models.basic_models import ProfilageResult
from data.models.basic_models import SemanticResult
from data.models.basic_models import SyntacticResult
from data.services.profilage.interfaces import ProfilageInterface
from data.services.profilage.utils import get_Dominant_Category
from data.services.profilage.utils import get_Dominant_subcategory


class ProfilageAnalyser(ProfilageInterface):
    """contains services for Profilage"""

    def __init__(self, df, document_id):
        super().__init__()
        self.df = df
        self.document_id = document_id

    def detect_null_values(self):
        """return position of null values"""
        df = self.df
        columns = df.columns
        result = [None] * len(columns)
        null_values = SyntacticResult.objects.get(document_id=self.document_id, rule=M100_3).result
        for i in range(len(columns)):
            if null_values[columns[i]]:
                col_null = [
                    (i, j) for j in range(len(df[columns[i]])) if df[columns[i]].isnull().iloc[j]
                ]
                result[i] = col_null

        # save null values (i,j) in database
        ProfilageResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M100_4,
            defaults={"result": result},
        )

    def detect_invalid_values_according_categories(self):
        """returns position of invalid values according to categories"""
        Dom_cat = get_Dominant_Category(self.document_id)
        indexes = SemanticResult.objects.get(document_id=self.document_id, rule=M104_28).result
        result = [None] * len(self.df.columns)
        for i, (column_key, column_value) in enumerate(indexes.items()):
            list_index = []
            category = list(Dom_cat[column_key].keys())[0]
            for key, value in column_value.items():
                if value[0] != category:
                    list_index.append(ast.literal_eval(key))
            if not list_index:
                list_index = None
            result[i] = list_index
        ProfilageResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M100_5,
            defaults={"result": result},
        )

    def detect_invalid_values_according_subcategories(self):
        """returns position of invalid values according to subcategories"""
        Dom_subcat = get_Dominant_subcategory(self.document_id)
        indexes = SemanticResult.objects.get(document_id=self.document_id, rule=M104_28).result
        result = [None] * len(self.df.columns)
        for i, (column_key, column_value) in enumerate(indexes.items()):
            list_index = []
            subcategory = list(Dom_subcat[column_key].keys())[0]
            for key, value in column_value.items():
                if value[1] != subcategory:
                    list_index.append(ast.literal_eval(key))
            if not list_index:
                list_index = None
            result[i] = list_index
        ProfilageResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M100_6,
            defaults={"result": result},
        )
