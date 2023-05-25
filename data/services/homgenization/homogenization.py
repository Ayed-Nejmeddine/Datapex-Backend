"""
    Homogenization
"""
import json

from django.conf import settings

import pandas as pd
import unidecode
from fuzzywuzzy import process
from pandas.api.types import is_string_dtype

from data.models import M103_3
from data.models import M103_30
from data.models import M105_5
from data.models import M112
from data.models import M113
from data.models import M114
from data.models import M115
from data.models import M116
from data.models import M117
from data.models import M118
from data.models import M119
from data.models import M120
from data.models import M121
from data.models import PHYSICAL_METRICS
from data.models.basic_models import DataDict
from data.models.basic_models import RegularExp
from data.models.basic_models import SemanticResult
from data.services.homgenization.interfaces import HomogenizationInterface
from data.services.homgenization.utils import get_Data_Dict
from data.services.homgenization.utils import get_db_result
from data.services.homgenization.utils import get_Dominant_Category_subcategory
from data.services.homgenization.utils import to_date
from data.services.homgenization.utils import transform_unite


class HomogenizationAnalyser(HomogenizationInterface):
    """contains services for Homogenization"""

    def __init__(self, df, document_id, document_path):
        super().__init__()
        self.df = df
        self.document_id = document_id
        self.document_path = document_path

    def remove_extra_spaces(self):
        """remove extra spaces for every value"""
        self.df = self.df.applymap(lambda x: " ".join(x.split()) if isinstance(x, str) else x)

    def remove_duplicated_rows(self):
        """remove duplications"""
        self.df = self.df.drop_duplicates()

    def standardisation_date(self):
        """format the dates to the format of the dominant format of the dates in this column"""
        document_id = self.document_id
        date_formats = [
            "%m %d %Y",
            "%m %d %y",
            "%d %b %Y",
            "%d/%m/%Y",
            "%H:%M:%S",
            "%Y-%m-%d",
            "%m/%d/%Y %H:%M",
            "%m/%d/%Y %H:%M:%S",
            "%B",
            "%A",
        ]
        rules = [M112, M113, M114, M115, M116, M117, M118, M119, M120, M121]
        date_result = [get_db_result(document_id, rule) for rule in rules]
        columns = list(date_result[0].result.keys())
        for col in columns:
            format_values = [i.result[col] for i in date_result]
            dominant_value = max(format_values)
            dominant_format = date_formats[format_values.index(dominant_value)]
            self.df[col] = (
                self.df[col].fillna("").apply(to_date, dominant_date_format=dominant_format)
            )

    def SubCategory_correction(self):
        """corrects the subcategories of each column"""
        Dom_cat, Dom_subcat = get_Dominant_Category_subcategory(self.document_id)
        columns = self.df.columns

        for col in columns:
            if not is_string_dtype(self.df[col].dtypes):
                continue

            self.df[col].fillna("", inplace=True)
            self.df[col] = self.df[col].apply(lambda x: unidecode.unidecode(str(x)))

            if Dom_cat[col] == "NON APPLICABLE" or Dom_subcat[col] == "NON APPLICABLE":
                continue

            category = list(Dom_cat[col].keys())[0]
            subCategory = list(Dom_subcat[col].keys())[0]
            data_list = get_Data_Dict(category)
            data_list_string = " ".join(str(x) for x in data_list)

            for _idx, value in self.df[col].iteritems():
                if str(value).upper() in data_list_string and not any(
                    obj[subCategory].lower() == value for obj in data_list
                ):
                    for obj in data_list:
                        if value.upper() in list(obj.values()):
                            self.df[col] = self.df[col].replace(value, obj[subCategory])

    def correction_unities(self):
        """correction des unités en abréviations"""
        df = self.df
        document_id = self.document_id
        dominants_categories = get_db_result(document_id, M103_3).result
        dominants_sub_categories = get_db_result(document_id, M105_5).result
        for column in dominants_categories:
            category = list(dominants_categories[column].keys())[0]
            if category in PHYSICAL_METRICS:
                subcategory = list(dominants_sub_categories[column].keys())[0]
                regexp = RegularExp.objects.filter(subcategory=subcategory).values_list(
                    "expression", flat=True
                )
                abreviation = regexp[0].split(r"\s")[1].strip("?").strip("+(").split("|")[0]
                self.df[column] = (
                    df[column].fillna("").apply(transform_unite, abreviation=abreviation)
                )

    def cleaning_document(self):
        """save changes tob  the new file"""
        df = self.df
        document_path = self.document_path
        full_document_path = settings.BASE_DIR + "/media/" + str(document_path)
        with open(full_document_path, "w") as document:
            df.to_csv(document, index=False, na_rep="", line_terminator="\n", sep=";")
        return full_document_path

    def data_correction(self):
        """correction data"""
        df = self.df
        columns = df.columns
        # semantic result to get the dominant categories
        semantic_result = SemanticResult.objects.get(document=self.document_id, rule=M103_30)
        semantic_result_values = semantic_result.result.values()
        # List of dominant categories
        columns_dominant_categories = []
        for item in semantic_result_values:
            if isinstance(item, dict):
                columns_dominant_categories.append(list(item.keys())[0])

        for category, column in zip(columns_dominant_categories, columns):
            # Import data from dictionary by category
            data_dict = DataDict.objects.filter(category=category)
            for data in data_dict:
                json_data_dict = json.loads(data.data_dict)
                # remove duplicated values from a list and combine all the values into a single list data_dict_unique_values
                data_dict_values = [
                    set(json_data_dict[i].values()) for i in range(len(json_data_dict))
                ]
                all_elements = set().union(*data_dict_values)
                data_dict_unique_values = list(all_elements)
                # search of each value in the dictionnary and replace it by the most similar one
            for i, word in enumerate(df[column]):
                characters_to_check = ["/", "@", "°"]
                if (
                    isinstance(word, str)
                    and not pd.isna(word)
                    and not any(char in word for char in characters_to_check)
                ):
                    # detect closest words in the dictionary
                    similars = []
                    for dict_word in data_dict_unique_values:
                        if word.upper() in dict_word:
                            similars.append(dict_word)
                        else:
                            if dict_word in word.upper():
                                similars.append(dict_word)
                    closest_match = process.extractOne(word, similars)
                    if closest_match:
                        closest_word = closest_match[0]
                        self.df.at[i, column] = closest_word
