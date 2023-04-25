"""Here all string functions"""
from threading import Thread
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from pandas.api.types import is_string_dtype

from data.models import COLUMN_TYPE
from data.models import DATA_TYPES
from data.models import FINISHED_STATE
from data.models import M102_17
from data.models import M102_2
from data.models import M102_26
from data.models import M103_18
from data.models import M103_3
from data.models import M104_4
from data.models import M105_5
from data.models import M106_6
from data.models import M103_26
from data.models import M104_19
from data.models import M105_8
from data.models import M105_20
from data.models import M106_9
from data.models import M107_10
from data.models import M108_11
from data.models import M101_1
from data.models import STRING_ANALYSIS
from data.models import MATCHED_EXPRESSIONS
from data.models.basic_models import AnalysisTrace
from data.models.basic_models import DataDict
from data.models.basic_models import Link
from data.models.basic_models import RegularExp
from data.models.basic_models import SemanticData
from data.models.basic_models import SyntacticResult
from data.services.syntactic.interfaces import StringInterface
from data.services.syntactic.utils import check_bool
from data.services.syntactic.utils import get_data_dict
from data.services.syntactic.utils import get_regexp
from data.services.syntactic.utils import model_text


class  StringAnalyser(StringInterface, Thread):
    """contains services for StringInterface"""

    def __init__(self, df, document_id):
        self.df = df
        self.document_id = document_id
        Thread.__init__(self)

    def get_min_length(self):
        """indicator for min length"""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].fillna("").str.len().min()
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M102_17,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        return res

    def get_max_length(self):
        """indicator for max length"""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].fillna("").str.len().max()
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M103_18,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        return res

    def get_average_length(self):
        """indicator for average length"""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].fillna("").str.len().mean()
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M104_19,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        return res

    def number_of_words(self, s_t=" "):
        """indicator of number of words."""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].fillna("").str.split(s_t).apply(len).sum()
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M105_8,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        return res

    def frequency_table(self):
        """String type indicator."""
        df = self.df
        columns = df.columns
        res = []
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                bool_mask = df[i].apply(check_bool)
                df = df[~bool_mask]
                alpha_mask = df[i].fillna("").str.contains("[a-zA-Z]")
                df_alpha = df[alpha_mask]
                strings = df_alpha[i].tolist()
                res.append(strings)
            else:
                res.append("None")
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M105_20,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        return res

    def count_number_of_words(self, s=" "):
        """indicator of number of words."""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                res[columns.get_loc(i)] = df[i].fillna("").str.split(s).apply(len).sum()
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M105_8,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        return res

    def count_values(self):
        """String type indicator."""
        df = self.df
        columns = df.columns
        res = np.zeros(len(columns), dtype=int)
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                bool_mask = df[i].apply(check_bool)
                df = df[~bool_mask]
                alpha_mask = df[i].fillna("").str.contains("[a-zA-Z]")
                df_alpha = df[alpha_mask]
                res[columns.get_loc(i)] = df_alpha[i].count()
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M108_11,
            defaults={"result": {i: res[columns.get_loc(i)] for i in columns}},
        )
        return res

    def model_data_frequency(self):
        """model the data and count the number of occurrences and percentage for the models"""
        df = self.df
        columns = df.columns
        percentages = []
        occurrences = []
        data_model = []
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                modeled_df = df[i].fillna("").apply(model_text)
                percentages.append(modeled_df.value_counts(normalize=True) * 100)
                occurrences.append(modeled_df.value_counts())
                data_model.append(np.array(modeled_df.value_counts().axes))
            else:
                data_model.append("None")
                occurrences.append(0)
                percentages.append(0)

        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M107_10,
            defaults={"result": {i: data_model[columns.get_loc(i)] for i in columns}},
        )
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M106_9,
            defaults={
                "result": {
                    i: (occurrences[columns.get_loc(i)], percentages[columns.get_loc(i)])
                    for i in columns
                }
            },
        )

        return data_model, percentages, occurrences

    
    def syntactic_validation_with_regexp(self):
        """Returns the number of categories and subcategories in each column"""
        df = self.df
        columns = df.columns
        expressions = RegularExp.objects.all().values_list("expression", flat=True)
        total_categorie_list=[]
        total_number_categorie_list=[]
        total_subcategorie_list=[]
        total_number_subcategorie_list=[]
        total_dominant_category_list=[]
        total_dominant_subcategory_list=[]
        
        for col in columns:
            res=[]
            dominant_category=""
            dominant_number_category=0
            
            
            if is_string_dtype(self.df[col].dtype):
                res=(df[col].apply(get_regexp,expressions=expressions)).tolist()
            
            list_cat = []
            nbre_cat = [0]*10
            list_subcat = []
            nbre_subcat = [0]*10
            for x in res:
                    if (x[0] not in list_cat) and x[0]:
                        list_cat.append(x[0])
                        index=list_cat.index(x[0])
                        nbre_cat[index] += 1
                    elif x[0]:
                        nbre_cat[list_cat.index(x[0])] += 1
                        
                    if x[1] not in list_subcat and x[1]:
                        list_subcat.append(x[1])
                        index=list_subcat.index(x[1])
                        nbre_subcat[index] += 1
                    elif x[1]:
                        nbre_subcat[list_subcat.index(x[1])] += 1
            total_categorie_list.append(list_cat)
            total_number_categorie_list.append(nbre_cat)
            
            dominant_number_category=max(nbre_cat)
            if dominant_number_category:
                dominant_category=list_cat[nbre_cat.index(dominant_number_category)]
                total_dominant_category_list.append((dominant_category,dominant_number_category)) #tuple(dominant category,it's number)
            else:
                total_dominant_category_list.append((None,None))
            
            total_categorie_list.append(list_subcat)
            total_number_categorie_list.append(nbre_subcat)
            dominant_number_subcategory=max(nbre_subcat)
            if dominant_number_subcategory:
                dominant_subcategory=list_subcat[nbre_cat.index(dominant_number_subcategory)]
                total_dominant_subcategory_list.append((dominant_subcategory,dominant_number_subcategory)) #tuple(dominant subcategory,it's number)
            
            else:
                total_dominant_subcategory_list.append((None,None))
            
            total_subcategorie_list.append(list_subcat)
            total_number_subcategorie_list.append(nbre_subcat)
        # number of MATCHED_EXPRESSIONS of data according to regexp
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=MATCHED_EXPRESSIONS,
            defaults = {
                "result": {
                    i: {"categories":{total_categorie_list[columns.get_loc(i)][j]:(total_number_categorie_list[columns.get_loc(i)][j]*100/len(df[i]))for j in range(len(total_categorie_list[columns.get_loc(i)]))}
                        }
                    for i in self.df.columns
                }
            }
                    )

        # number of categories of data according to regexp
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M101_1,
            defaults={"result": {
        i: {"categories":
            len(total_categorie_list[columns.get_loc(i)])
       
        }
        for i in self.df.columns} }
        
        )
        # number of subcategories of data according to regexp
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M102_2,
            defaults={"result": {
        i: {"subcategories":
            len(total_subcategorie_list[columns.get_loc(i)])
       
        }
        for i in self.df.columns
    }},
        )

        # Number of semantically valid values according to the dominant category
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M103_3,
            defaults={"result": {
        i:{"valid_values(category)":{total_dominant_category_list[columns.get_loc(i)][0]:total_dominant_category_list[columns.get_loc(i)][1]}
         }for i in self.df.columns}}
        )
        # Number of semantically invalid values according to the dominant category
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M104_4,
            defaults={"result": {
        i:{"invalid_values(category)":{total_dominant_category_list[columns.get_loc(i)][0]:len(df[i])-(total_dominant_category_list[columns.get_loc(i)][1]or 0)}
         }for i in self.df.columns}})

        # Number of semantically valid values according to the dominant category
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M105_5,
            defaults={"result": {
        i:{"valid_values(subcategory)":{total_dominant_subcategory_list[columns.get_loc(i)][0]:total_dominant_subcategory_list[columns.get_loc(i)][1]}
         }for i in self.df.columns}}
        )
        # Number of semantically invalid values according to the dominant category
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M106_6,
            defaults={"result": {
        i:{"invalid_values(subcategory)":{total_dominant_subcategory_list[columns.get_loc(i)][0]:len(df[i])-(total_dominant_subcategory_list[columns.get_loc(i)][1]or 0)}
         }for i in self.df.columns}})

        
        
    
        return total_categorie_list,total_number_categorie_list

    def syntactic_validation_with_data_dict(self):
        """
        Syntactically validate the data according to the data dictionary.
        res is an array of the number of syntactically valid data according to the data dictionary.
        invalid_res is an array of the number of syntactically invalid data according to the data dictionary.
        data_types will contain the data types of each column (exp: city, airport, firstname, etc...) and percentages will contain the percentages of
        the data_types in each column.
        """
        df = self.df
        columns = df.columns
        invalid_res = np.full(len(columns), np.array(df.shape[0]))
        #  TODO: Matching with the data dict takes a long time due to the size of the data_dict.  # pylint: disable=W0511
        data_types = []
        percentages = []
        column_type = []
        total_dict = []
        for i in columns:
            if is_string_dtype(df[i].dtypes):
                d = (
                    df[i]
                    .value_counts(dropna=False)
                    .keys()
                    .to_series()
                    .apply(get_data_dict, data_dict=DataDict.objects.all())
                )
                column_type.append(d)
                matched_res = d.apply(lambda x: ("no-match", "no-match") if x is None else x)
                matched_dict = {}
                percentage = df[i].value_counts(dropna=False, normalize=True) * 100
                for j in range(len(matched_res)):
                    if matched_res[j] in matched_dict.keys():
                        matched_dict[matched_res[j]] += percentage[j]
                    else:
                        matched_dict[matched_res[j]] = percentage[j]

                data_types.append(matched_dict.keys())
                percentages.append(matched_dict.values())
                total_dict.append(matched_dict)
                invalid_res[columns.get_loc(i)] = df[i].value_counts(dropna=False)[d.isna()].sum()
            else:
                data_types.append(["non-applicable"])
                percentages.append([0])
                column_type.append([])
                total_dict.append({})
        res = np.array(df.shape[0]) - invalid_res
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M102_26,
            defaults={"result": {i: res[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=DATA_TYPES,
            defaults={
                "result": {
                    i: (data_types[columns.get_loc(i)], percentages[columns.get_loc(i)])
                    for i in columns
                }
            },
        )
        # number of syntactically invalid data according to the data dictionary
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=M103_26,
            defaults={
                "result": {i: invalid_res[self.df.columns.get_loc(i)] for i in self.df.columns}
            },
        )
        return column_type, total_dict

    def get_columns_type(self):
        """Get an estimate of the column type"""
        _, data_matching_dict = self.syntactic_validation_with_data_dict()
        regexp_column_type, regexp_matching_dict = self.syntactic_validation_with_regexp()
        matched_res = []
        res_types = []
        for i in range(len(regexp_column_type)):
            res = []
            most_matched_reg = max(regexp_matching_dict[i], key=regexp_matching_dict[i].get)
            most_matched_data = max(data_matching_dict[i], key=data_matching_dict[i].get)
            if most_matched_reg == ("no-match", "no-match"):
                res.append(most_matched_data)
                res_types.append("datadict")
            else:
                res.append(most_matched_reg)
                res_types.append("regexp")
            matched_res.append(res)
        SemanticData.objects.update_or_create(
            document_id=self.document_id,
            defaults={"data": {i: res_types[self.df.columns.get_loc(i)] for i in self.df.columns}},
        )
        SyntacticResult.objects.update_or_create(
            document_id=self.document_id,
            rule=COLUMN_TYPE,
            defaults={
                "result": {i: matched_res[self.df.columns.get_loc(i)] for i in self.df.columns}
            },
        )

    def link(self):
        """
        Define the links between columns of the type string by calculating the rate of
        similarity between these columns.
        For example two columns with identical values have a similarity score of 100%.
        """
        df = self.df
        columns = df.columns
        for col1 in columns:
            for col2 in columns[columns.get_loc(col1) + 1 :]:
                s = df[col1].apply(fuzz.token_set_ratio, s2=df[col2]).mean()
                if is_string_dtype(df[col1].dtypes) and is_string_dtype(df[col2].dtypes) and s > 80:
                    Link.objects.update_or_create(
                        document_id=self.document_id,
                        first_column=col1,
                        second_column=col2,
                        defaults={"relationship": str(s) + "% similarity score"},
                    )

    def run(self):
        self.get_min_length()
        self.get_max_length()
        self.get_average_length()
        self.frequency_table()
        self.count_number_of_words()
        self.count_values()
        self.model_data_frequency()
        self.get_columns_type()
        AnalysisTrace.objects.update_or_create(
            document_id=self.document_id,
            analysis_type=STRING_ANALYSIS,
            defaults={"state": FINISHED_STATE},
        )
        self.link()
