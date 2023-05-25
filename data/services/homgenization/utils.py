"""utils of homogenization"""
import datetime
import json

from cachetools import TTLCache
from cachetools import cached

from data.models import M103_30
from data.models import M103_31
from data.models.basic_models import DataDict
from data.models.basic_models import SemanticResult
from data.models.basic_models import SyntacticResult

cache = TTLCache(maxsize=200, ttl=86400)


def get_db_result(document_id, rule):
    """get syntactic result from db"""
    return SyntacticResult.objects.get(document=document_id, rule=rule)


def to_date(date_text, dominant_date_format):
    """transform the date value to the dominant date format"""
    date_formats = [
        "%d-%m-%Y",
        "%I-%M-%S",
        "%m %d %Y",
        "%A",
        "%m %d %y",
        "%d-%m-%y %H:%M:%S",
        "%d %b %Y",
        "%d/%m/%Y",
        "%H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%d",
        "%m/%d/%Y %H:%M",
        "%m/%d/%Y %H:%M:%S",
        "%B",
        "%Y/%m/%d",
        "%Y/%m/%d %H:%M",
        "%d-%m-%y",
        "%b %d, %Y",
        "%Y-%m-%d %H:%M:%S",
        "%b",
        "%a",
        "%A,%d %B, %Y",
        "%d-%b-%Y",
        "%a,%d %b, %Y",
        "%H-%M-%S",
    ]
    date_object = ""
    for forme in date_formats:
        try:
            date_object = datetime.datetime.strptime(date_text, forme)
            return date_object.strftime(dominant_date_format)
        except ValueError:
            continue
    return date_text


def get_Dominant_Category_subcategory(doc_id):
    """get the semantic analysis of a document"""
    Dom_cat = SemanticResult.objects.get(rule=M103_30, document_id=doc_id).result
    Dom_subcat = SemanticResult.objects.get(rule=M103_31, document_id=doc_id).result
    return Dom_cat, Dom_subcat


@cached(cache)
def get_Data_Dict(category):
    """Retreives the data dictionary from the database"""
    data_dict = DataDict.objects.filter(category=category).values_list("data_dict", flat=True)
    List_rows = [json.loads(data) for data in data_dict]
    data_list = [obj for data in List_rows for obj in data]
    return data_list
