import re
import json

import pandas as pd

def get_regexp(value, expressions):
    """Get the matching regular expression."""
    if not pd.isnull(value):
        
        for exp in expressions:
            if isinstance(value, str):
                cat = re.search(exp[2], value.upper())
                if cat:
                    return (exp[0], exp[1])
            elif not isinstance(value, bool):
                
                cat = re.search(exp[2], str(value))
                if cat:
                    return (exp[0], exp[1])
    return ("no-match", "no-match")

def get_data_dict(text, data_dict):
    """Get the matching data dictionary."""
    if not pd.isnull(text):
        text = " ".join(text.split())
        for data in data_dict:
            if text.upper() in data.data_dict:
                json_data_dict = json.loads(data.data_dict)
                for row in json_data_dict:
                    for sub, val in row.items():
                        if text.upper() == val:
                            return (row["CATEGORY"], sub)
    return ("no-match", "no-match")