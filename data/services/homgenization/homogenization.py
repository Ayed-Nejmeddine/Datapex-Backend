"""
    Homogenization
"""
import pandas as pd
from data.models.basic_models import DataDict,SemanticResult
import os
import json
from django.conf import settings
from data.services.homgenization.interfaces import HomogenizationInterface
from data.models import M103_30
from pandas.api.types import is_string_dtype
import Levenshtein as lev
from fuzzywuzzy import process

class HomogenizationAnalyser(HomogenizationInterface):
    """contains services for Homogenization"""

    def __init__(self, df, document_id, document_path):
        super().__init__()
        self.df = df
        self.document_id = document_id
        self.document_path = document_path
    
    def remove_extra_spaces(self):
        self.df = self.df.applymap(lambda x: ' '.join(x.split()) if isinstance(x, str) else x)
    
    
    def remove_duplicated_rows(self):
        self.df = self.df.drop_duplicates()
        
        
    def cleaning_document(self):
        df=self.df
        document_path=self.document_path
        full_document_path = (settings.BASE_DIR+'/media/'+str(document_path))
        with open(full_document_path, "w") as document:
            df.to_csv(document,index=False,na_rep='', line_terminator='\n',sep=';')
        return full_document_path
    
    def data_correction(self):
        df=self.df
        columns=df.columns
        # semantic result to get the dominant categories
        semantic_result = SemanticResult.objects.get(document=self.document_id ,rule= M103_30)
        semantic_result_values = semantic_result.result.values()
        # List of dominant categories
        columns_dominant_categories =[]
        for item in semantic_result_values:
            if isinstance(item, dict):
                columns_dominant_categories.append (list(item.keys())[0])

        for category,column in zip(columns_dominant_categories,columns):
            # Import data from dictionary by category
            data_dict = DataDict.objects.filter( category = category)
            for data in data_dict:
                json_data_dict = json.loads(data.data_dict)
                # remove duplicated values from a list and combine all the values into a single list data_dict_unique_values
                data_dict_values = [ set(json_data_dict[i].values()) for i in range(len(json_data_dict))]
                all_elements = set().union(*data_dict_values)
                data_dict_unique_values= list(all_elements)
                # search of each value in the dictionnary and replace it by the most similar one
            for i, word in enumerate(df[column]):
                characters_to_check=['/','@','°']
                if isinstance(word, str) and not pd.isna(word) and not any(char in word for char in characters_to_check):
                    # detect closest words in the dictionary
                    similars =[]
                    for dict_word in data_dict_unique_values:
                        if word.upper() in dict_word:
                            similars.append(dict_word)
                        else :
                            if dict_word in word.upper():
                                similars.append(dict_word)
                    closest_match = process.extractOne(word, similars)
                    if closest_match:
                        closest_word = closest_match[0]
                        self.df.at[i, column] = closest_word
                                                