import json
import re

from cachetools import TTLCache
from cachetools import cached

from data.models import M103_30
from data.models import M103_31
from data.models.basic_models import DataDict
from data.models.basic_models import SemanticResult

cache = TTLCache(maxsize=200, ttl=86400)


@cached(cache)
def get_Data_Dict(category):
    """Retreives the data dictionary from the database"""
    data_dict = DataDict.objects.filter(category=category).values_list("data_dict", flat=True)
    List_rows = [json.loads(data) for data in data_dict]
    data_list = [obj for data in List_rows for obj in data]
    return data_list


def get_Dominant_Category_subcategory(doc_id):
    """get the semantic analysis of a document"""
    Dom_cat = SemanticResult.objects.get(rule=M103_30, document_id=doc_id).result
    Dom_subcat = SemanticResult.objects.get(rule=M103_31, document_id=doc_id).result
    return Dom_cat, Dom_subcat


def check_match_data_dict_cat(values, category, i):
    """check if the values exist in the data dictionary of the dominant category"""
    res = []
    data_list = get_Data_Dict(category)
    data_list_string = "".join(str(x) for x in data_list)
    for idx, value in values.iteritems():
        if str(value).upper() not in data_list_string:
            res.append((idx, i))
    return res


def check_match_data_dict_subcat(values, category, i, subCategory):
    """check if the values exist in the data dictionary of the dominant subcategory"""
    res = []
    data_list = get_Data_Dict(category)
    data_list_string = "".join(str(x) for x in data_list)
    for idx, value in values.iteritems():
        if str(value).upper() in data_list_string and not any(
            obj[subCategory] == str(value).upper() for obj in data_list
        ):
            res.append((idx, i))
    return res


def check_match_reg(value, expressions):
    """check if the values match the regular expressions"""
    if any(re.match(exp[0], str(value).upper()) for exp in expressions):
        return True
    return False


def check_category(category):
    """check the dominant category exist in the data dictionary"""
    categories = DataDict.objects.values_list("category", flat=True)
    if category in categories:
        return True
    return False
