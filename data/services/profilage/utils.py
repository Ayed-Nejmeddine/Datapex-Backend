import json

from cachetools import TTLCache
from cachetools import cached

from data.models import M103_3
from data.models import M105_5
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


def get_Dominant_subcategory(doc_id):
    """get the semantic analysis of a document"""
    Dom_subcat = SemanticResult.objects.get(rule=M105_5, document_id=doc_id).result
    return Dom_subcat


def get_Dominant_Category(doc_id):
    """get the semantic analysis of a document"""
    Dom_cat = SemanticResult.objects.get(rule=M103_3, document_id=doc_id).result
    return Dom_cat
