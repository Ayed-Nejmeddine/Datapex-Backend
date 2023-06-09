from threading import Thread
from data.services.semantic.analyser import SemanticAnalyser
import pandas as pd


class Analyser(SemanticAnalyser, Thread):

    def __init__(self, document):
        self.document_id = document.id
        reader = pd.read_csv(document.document_path, sep=";",encoding='latin-1')
        df = pd.DataFrame(reader)
        df = df.convert_dtypes()
        columns = df.columns
        num_col = []
        date_col = []
        string_col = []
        for i in columns:
            if pd.to_numeric(df[i], errors='coerce').any():
                num_col.append(i)
            elif df[i].apply(pd.to_datetime, errors='coerce').count() > 0:
                date_col.append(i)
            else:
                string_col.append(i)
        self.df = df[string_col]
        Thread.__init__(self)

    def run(self):
        self.count_number_of_categories_and_subcategories()
        self.count_validation_percentages()
