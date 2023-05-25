"""Homogenization init"""
from threading import Thread

import pandas as pd

from data.services.homgenization.homogenization import HomogenizationAnalyser


class Homogenization(HomogenizationAnalyser, Thread):
    """ "Homogenization function"""

    def __init__(self, document):
        super().__init__(df=None, document_id=None, document_path=None)
        self.document_id = document.id
        self.document_path = document.document_path
        with document.document_path.open("r") as f:
            df = pd.read_csv(f, sep=";")
            df = df.convert_dtypes()
        self.df = df
        Thread.__init__(self)

    def run(self):
        self.remove_extra_spaces()
        self.remove_duplicated_rows()
        self.standardisation_date()
        self.SubCategory_correction()
        self.cleaning_document()
