"""Profilage init"""
from threading import Thread

import pandas as pd

from data.services.profilage.profilage import ProfilageAnalyser


class Profilage(ProfilageAnalyser, Thread):
    """ "Profilage function"""

    def __init__(self, document):
        super().__init__(df=None, document_id=None)
        self.document_id = document.id
        self.document_path = document.document_path
        with document.document_path.open("r") as f:
            df = pd.read_csv(f, sep=";")
            df = df.convert_dtypes()
        self.df = df
        Thread.__init__(self)

    def run(self):
        self.detect_null_values()
        self.detect_invalid_values_according_categories()
        self.detect_invalid_values_according_subcategories()
