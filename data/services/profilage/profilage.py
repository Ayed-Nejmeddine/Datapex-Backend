"""
    Profilage
"""
import unidecode

from data.models import M100_3
from data.models import M100_4
from data.models import M103_30
from data.models import M104_5
from data.models import M104_26
from data.models import M104_27
from data.models.basic_models import ProfilageResult
from data.models.basic_models import RegularExp
from data.models.basic_models import SemanticResult
from data.models.basic_models import SyntacticResult
from data.services.profilage.interfaces import ProfilageInterface
from data.services.profilage.utils import check_category
from data.services.profilage.utils import check_match_data_dict_cat
from data.services.profilage.utils import check_match_data_dict_subcat
from data.services.profilage.utils import check_match_reg
from data.services.profilage.utils import get_Dominant_Category_subcategory


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
        df = self.df
        columns = df.columns
        result = [None] * len(columns)
        Dom_cat = SemanticResult.objects.get(rule=M103_30, document_id=self.document_id).result
        invalid_values = SemanticResult.objects.get(
            document_id=self.document_id, rule=M104_5
        ).result
        for i in range(len(columns)):
            res = []
            values = df[columns[i]].dropna()
            if invalid_values[columns[i]].values != 0:
                if Dom_cat[columns[i]] == "NON APPLICABLE":
                    continue
                df[columns[i]] = df[columns[i]].apply(lambda x: unidecode.unidecode(str(x)))
                category = list(Dom_cat[columns[i]].keys())[0]
                if check_category(category):
                    res = check_match_data_dict_cat(values, category, i)
                elif category != "no-match":
                    expressions = RegularExp.objects.filter(category=category).values_list(
                        "expression"
                    )
                    for idx, value in values.iteritems():
                        if not check_match_reg(value, expressions):
                            res.append((idx, i))
                if not res:
                    res = None
                result[i] = res
        # save null values (i,j) in database
        ProfilageResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M104_26,
            defaults={"result": {i: result[columns.get_loc(i)] for i in columns}},
        )

    def detect_invalid_values_according_subcategories(self):
        """returns position of invalid values according to subcategories"""
        df = self.df
        Dom_cat, Dom_subcat = get_Dominant_Category_subcategory(self.document_id)
        columns = df.columns
        result = [None] * len(columns)
        for i in range(len(columns)):
            res = []
            values = df[columns[i]].dropna()
            df[columns[i]] = df[columns[i]].apply(lambda x: unidecode.unidecode(str(x)))
            if (
                Dom_cat[columns[i]] == "NON APPLICABLE"
                or Dom_subcat[columns[i]] == "NON APPLICABLE"
            ):
                continue
            category = list(Dom_cat[columns[i]].keys())[0]
            subCategory = list(Dom_subcat[columns[i]].keys())[0]
            if check_category(category):
                res = check_match_data_dict_subcat(values, category, i, subCategory)
            elif subCategory != "no-match":
                expressions = RegularExp.objects.filter(subcategory=subCategory).values_list(
                    "expression"
                )
                for idx, value in values.iteritems():
                    if not check_match_reg(value, expressions):
                        res.append((idx, i))
            if not res:
                res = None
            result[i] = res
        ProfilageResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M104_27,
            defaults={"result": {i: result[columns.get_loc(i)] for i in columns}},
        )
