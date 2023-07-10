"""
    SemanticAnalyser
    """
from data.models import M103_3
from data.models import M104_5
from data.models import M104_6
from data.models import M105_5
from data.models import M113_16
from data.models.basic_models import SemanticResult
from data.models.basic_models import SyntacticResult
from data.services.semantic.interfaces import SemanticInterface
from data.services.semantic.utils import get_data_dict
from data.models.basic_models import SemanticResult
from data.models.basic_models import RegularExp
from data.models.basic_models import DataDict
from data.models import M101_1

from data.services.semantic.interfaces import SemanticInterface
from data.services.syntactic import BaseAbstract
from data.services.semantic.utils import get_regexp

class SemanticAnalyser(SemanticInterface):
    """contains services for SemanticInterface"""

    def __init__(self, df, document_id):
        super().__init__()
        self.df = df
        self.document_id = document_id

    def _detected_types(self, matched_dict_percentages):
        """detect category, subcategory and percentage of the column"""
        detected_types = []
        column_detected_types = []

        for tuple_value in matched_dict_percentages:
            if tuple_value not in detected_types:
                cat_sub_val = {
                    "CATEGORY": tuple_value[0],
                    "SUBCATEGORY": tuple_value[1],
                    "PERCENTAGE": matched_dict_percentages[tuple_value],
                }
                column_detected_types.append(cat_sub_val)
                detected_types.append(tuple_value)
            else:
                column_detected_types[detected_types.index(tuple_value)][
                    "PERCENTAGE"
                ] += matched_dict_percentages[tuple_value]
        return column_detected_types

    def _detected_categories(self, column_detected_types):
        """detected categories in the column"""
        column_detected_category = {}
        for col_type in column_detected_types:
            if col_type["CATEGORY"] not in column_detected_category:
                column_detected_category[col_type["CATEGORY"]] = col_type["PERCENTAGE"]
            else:
                column_detected_category[col_type["CATEGORY"]] += col_type["PERCENTAGE"]
        return column_detected_category

    def _column_dominant_category(self, column_detected_category):
        """detect the dominant category in the column"""
        result_dict = {}
        for key in column_detected_category:
            if column_detected_category[key] == max(column_detected_category.values()):
                result_dict[key] = column_detected_category[key]
                break
        return result_dict

    def _column_dominant_subcategory(self, column_dominant_categories, column_detected_types):
        """detect the dominant subcategory in the column"""
        column_dominant_sub_categories = {}
        if column_dominant_categories:
            maxVal = 0
            first_key = next(iter(column_dominant_categories.keys()))
            for col_type in column_detected_types:
                if col_type["CATEGORY"] == first_key and col_type["PERCENTAGE"] > maxVal:
                    maxVal = col_type["PERCENTAGE"]
                    sub_cat = col_type["SUBCATEGORY"]
            column_dominant_sub_categories[sub_cat] = maxVal
            return column_dominant_sub_categories

        return "NON APPLICABLE"

    def _update_or_create_db(self, columns, rule, result):
        """updates or create a database row using the rule"""
        SemanticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=rule,
            defaults={"result": {i: result[columns.get_loc(i)] for i in columns}},
        )

    def semantic_validation(self):
        """Returns the number of categories and subcategories in each column accorging to regexp and datadict"""
        df = self.df
        columns = df.columns
        expressions = RegularExp.objects.all().values_list("category", "subcategory", "expression")
        data_dict = DataDict.objects.all()
        global_detected_categories = []
        global_dominant_categories = []
        global_dominant_subcategories = []
        for i in columns:
            df[i] = df[i].apply(lambda x: str(x).replace("Â°", "°"))
            data_serie=[]
            for j in df[i]:
                regex_result=get_regexp(j,expressions=expressions)
                if regex_result!= ("no-match","no-match") :
                    data_serie.append(regex_result)
                else:
                    dict_result=get_data_dict(j,data_dict)
                    data_serie.append(dict_result)
            matched_dict = {cat_sub: data_serie.count(cat_sub) for cat_sub in data_serie}
            matched_dict_percentages = {
                key: round(int(matched_dict[key] * 100 / len(df[i])), 2) for key in matched_dict
            }
            column_detected_types = self._detected_types(matched_dict_percentages)
            column_detected_category = self._detected_categories(column_detected_types)
            global_detected_categories.append(column_detected_category)
            # the determination of the dominant category will be changed and we will consider the percentage of the dominant catgeory must be greater than 50%
            column_dominant_categories = self._column_dominant_category(column_detected_category)
            global_dominant_categories.append(column_dominant_categories)
            column_dominant_sub_categories = self._column_dominant_subcategory(
                column_dominant_categories, column_detected_types
            )
            global_dominant_subcategories.append(column_dominant_sub_categories)
        # print(global_dominant_categories)
        self._update_or_create_db(columns, M101_1, global_detected_categories)
        self._update_or_create_db(columns, M103_3, global_dominant_categories)
        self._update_or_create_db(columns, M105_5, global_dominant_subcategories)

        return (
            global_detected_categories,
            global_dominant_categories,
            global_dominant_subcategories,
        )

    def count_validation_percentages(self):
        """Count the percentage of the semantically valid and invalid to the dominant category and subcategory"""
        df = self.df
        columns = df.columns
        dom_cat_res = self.semantic_validation()[1]
        dom_sub_cat_res = self.semantic_validation()[2]
        rows = SyntacticResult.objects.get(document_id=self.document_id, rule=M113_16)
        number_rows = rows.result["Rows"]
        
        if not number_rows:
            syntactic_analyser = BaseAbstract(self.df, self.document_id)
            syntactic_analyser.count_number_rows()
        # convert the percentages to numbers
        dom_cat ={
            k:{list(dom_cat_res[columns.get_loc(k)].keys())[0]: int(list(dom_cat_res[columns.get_loc(k)].values())[0] * number_rows / 100)}
                if dom_cat_res[columns.get_loc(k)] != "NON APPLICABLE"
                else {"no-match": number_rows}
                for k in columns}
   
        
        dom_sub_cat = {
            k:{list(dom_sub_cat_res[columns.get_loc(k)].keys())[0]: round(
                    list(dom_sub_cat_res[columns.get_loc(k)].values())[0] * number_rows / 100
                )}
            if dom_sub_cat_res[columns.get_loc(k)] != "NON APPLICABLE"
            else {"no-match": number_rows}
            for k in columns
        }
        
  
        invalid_dom_cat = {
            k: {list(dom_cat[k].keys())[0]: number_rows - int(list(dom_cat[k].values())[0])}
            for k in columns
        }
        
    
        invalid_dom_sub_cat = {
            k: {list(dom_sub_cat[k].keys())[0]: number_rows - list(dom_sub_cat[k].values())[0]}
            for k in columns 
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
