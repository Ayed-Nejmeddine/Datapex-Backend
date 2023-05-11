"""
    Homogenization
"""
import pandas as pd
import os
from django.conf import settings
from data.services.homgenization.interfaces import HomogenizationInterface
class HomogenizationAnalyser(HomogenizationInterface):
    """contains services for Homogenization"""

    def __init__(self, df, document_id, document_path):
        super().__init__()
        self.df = df
        self.document_id = document_id
        self.document_path = document_path
    
    def remove_duplicated_rows(self):
        df=self.df
        document_path=self.document_path
        df = df.replace(r'\s+', ' ', regex=True)
        df = df.drop_duplicates()
        print(document_path)
        print(settings.BASE_DIR)
        full_document_path = (settings.BASE_DIR+'/media/'+str(document_path))
        print(full_document_path)
        with open(full_document_path, "w") as document:
            df.to_csv(document, index=False)
        return full_document_path
    