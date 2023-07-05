"""
    Homogenization
"""
import json

from django.conf import settings

import numpy as np
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
from data.models import M200_1
from data.models import M200_3
from data.models import M200_4
from data.models import M200_5
from data.models import PHYSICAL_METRICS
from data.models.basic_models import DataDict
from data.models.basic_models import HomogenizationResult
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
        columns = self.df.columns
        result = [None] * len(columns)
        for col in date_result[0].result.keys():
            format_values = [i.result[col] for i in date_result]
            dominant_value = max(format_values)
            dominant_format = date_formats[format_values.index(dominant_value)]
            corrected_column = (
                self.df[col].fillna("").apply(to_date, dominant_date_format=dominant_format)
            )
            different_indices = np.where(corrected_column != self.df[col].fillna(""))[0]
            list_index = [(self.df.columns.get_loc(col), i) for i in different_indices]
            self.df[col] = corrected_column
            result[self.df.columns.get_loc(col)] = list_index
        HomogenizationResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M200_3,
            defaults={"result": result},
        )

    def SubCategory_correction(self):
        """corrects the subcategories of each column"""
        Dom_cat, Dom_subcat = get_Dominant_Category_subcategory(self.document_id)
        columns = self.df.columns
        result = [None] * len(self.df.columns)
        for i in range(len(columns)):
            list_index = []
            if not is_string_dtype(self.df[columns[i]].dtypes):
                continue
            self.df[columns[i]].fillna("", inplace=True)
            self.df[columns[i]] = self.df[columns[i]].apply(lambda x: unidecode.unidecode(str(x)))

            if (
                Dom_cat[columns[i]] == "NON APPLICABLE"
                or Dom_subcat[columns[i]] == "NON APPLICABLE"
            ):
                continue
            category = list(Dom_cat[columns[i]].keys())[0]
            subCategory = list(Dom_subcat[columns[i]].keys())[0]
            data_list = get_Data_Dict(category)
            data_list_string = " ".join(str(x) for x in data_list)
            for idx, value in self.df[columns[i]].iteritems():
                if str(value).upper() in data_list_string and not any(
                    obj[subCategory] == str(value).upper() for obj in data_list
                ):
                    for obj in data_list:
                        if value.upper() in list(obj.values()):
                            self.df[columns[i]] = self.df[columns[i]].replace(
                                value, obj[subCategory]
                            )
                            list_index.append((i, idx))
            if not list_index:
                list_index = None
            result[i] = list_index
        HomogenizationResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M200_1,
            defaults={"result": result},
        )

    def correction_unities(self):
        """correction des unités en abréviations"""
        df = self.df
        document_id = self.document_id
        dominants_categories = get_db_result(document_id, M103_3).result
        dominants_sub_categories = get_db_result(document_id, M105_5).result
        result = [None] * len(self.df.columns)
        for column in dominants_categories:
            category = list(dominants_categories[column].keys())[0]
            if category in PHYSICAL_METRICS:
                list_index = []
                subcategory = list(dominants_sub_categories[column].keys())[0]
                regexp = RegularExp.objects.filter(subcategory=subcategory).values_list(
                    "expression", flat=True
                )
                abreviation = regexp[0].split(r"\s")[1].strip("?").strip("+(").split("|")[0]
                corrected_column = (
                    df[column].fillna("").apply(transform_unite, abreviation=abreviation)
                )
                different_indices = np.where(corrected_column != self.df[column])[0]
                list_index = [(self.df.columns.get_loc(column), i) for i in different_indices]
                # list_index=compare_two_column(corrected_column,self.df[column])
                self.df[column] = corrected_column
                result[self.df.columns.get_loc(column)] = list_index
        HomogenizationResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M200_4,
            defaults={"result": result},
        )

    def cleaning_document(self):
        """save changes to  the new file"""
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
        result = [None] * len(self.df.columns)
        # semantic result to get the dominant categories
        semantic_result = SemanticResult.objects.get(document=self.document_id, rule=M103_30)
        semantic_result_values = semantic_result.result.values()
        # List of dominant categories
        columns_dominant_categories = []
        for item in semantic_result_values:
            if isinstance(item, dict):
                columns_dominant_categories.append(list(item.keys())[0])
        for category, column, idx in zip(columns_dominant_categories, columns, range(len(columns))):
            changed_indexes_list = []
            # Import data from dictionary by category
            data_dict = DataDict.objects.filter(category=category)
            data_dict_unique_values = []
            for data in data_dict:
                json_data_dict = json.loads(data.data_dict)
                # remove duplicated values from a list and combine all the values into a single list data_dict_unique_values
                data_dict_values = [
                    set(json_data_dict[i].values()) for i in range(len(json_data_dict))
                ]
                all_elements = set().union(*data_dict_values)
                data_dict_unique_values = list(all_elements)
            # search of each value in the dictionnary and replace it by the most similar one
            characters_to_check = ["/", "@", "°"]
            for i, word in enumerate(df[column]):
                if (
                    isinstance(word, str)
                    and not pd.isna(word)
                    and not any(char in word for char in characters_to_check)
                    and word.upper() not in data_dict_unique_values
                ):
                    closest_match = process.extractOne(word.upper(), data_dict_unique_values)
                    if closest_match and 60 < closest_match[1] < 100:
                        closest_word = closest_match[0]
                        self.df.at[i, column] = closest_word
                        changed_indexes_list.append((idx, i))
            if not changed_indexes_list:
                changed_indexes_list = None
            result[idx] = changed_indexes_list
        HomogenizationResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M200_5,
            defaults={"result": result},
        )
