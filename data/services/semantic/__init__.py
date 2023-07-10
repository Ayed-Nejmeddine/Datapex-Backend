from threading import Thread
from data.services.semantic.analyser import SemanticAnalyser
import pandas as pd


class Analyser(SemanticAnalyser, Thread):

    def __init__(self, document):
        self.document_id = document.id
        reader = pd.read_csv(document.document_path, sep=";",encoding='latin-1')
        df = pd.DataFrame(reader)
        self.df = df.convert_dtypes()

        Thread.__init__(self)

    def run(self):
        self.semantic_validation()
        self.count_validation_percentages()
