from threading import Thread
from data.services.semantic.analyser import SemanticAnalyser
import pandas as pd


class Analyser(SemanticAnalyser, Thread):

    def __init__(self, document):
        self.document_id = document.id
        with document.document_path.open('r') as f:
            df = pd.DataFrame(pd.read_csv(f))
            self.df = df.convert_dtypes()
        Thread.__init__(self)
