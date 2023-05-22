"""utils of homogenization"""
import datetime


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
