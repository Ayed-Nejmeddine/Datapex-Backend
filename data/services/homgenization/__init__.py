from threading import Thread
from data.services.homgenization.homogenization import HomogenizationAnalyser
import pandas as pd
from data.models import HOMOGENIZATION_DUPLICATION
from data.models import RUNNING_STATE
from data.models.basic_models import HomogenizationTrace


class Homogenization(HomogenizationAnalyser, Thread):

    def __init__(self, document):
        self.document_id = document.id
        self.document_path = document.document_path
        with document.document_path.open('r') as f:
            df = pd.read_csv(f,sep=';')
            df = df.convert_dtypes()
        self.df = df
        Thread.__init__(self)

    def run(self):
        self.remove_extra_spaces()
        self.remove_duplicated_rows()
        self.data_correction()
        self.cleaning_document()
        
    