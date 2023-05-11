from threading import Thread
from data.services.homgenization.homogenization import HomogenizationAnalyser
import pandas as pd


class Homogenization(HomogenizationAnalyser, Thread):

    def __init__(self, document):
        self.document_id = document.id
        self.document_path = document.document_path
        with document.document_path.open('r') as f:
            df = pd.DataFrame(pd.read_csv(f))
            df = df.convert_dtypes()
        columns = df.columns
        string_col = []
        for i in columns:
                string_col.append(i)
        self.df = df[string_col]
        Thread.__init__(self)

    def run(self):
        self.remove_duplicated_rows()
