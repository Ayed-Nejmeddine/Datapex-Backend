import pandas as pd
import json 
def get_data_dict(text, data_dict):
    """Get the matching data dictionary."""
    if not pd.isnull(text):
        text = " ".join(text.split())
        for data in data_dict:
            json_data_dict = json.loads(data.data_dict)
            for row in json_data_dict:
                for sub, val in row.items():
                    if text.upper() == val:
                        return (row["CATEGORY"], sub)

    return ("no-match", "no-match")