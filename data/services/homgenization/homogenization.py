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
    
    def remove_extra_spaces(self):
        df=self.df
        print(df.info())
        document_path=self.document_path
        df = df.applymap(lambda x: ' '.join(x.split()) if isinstance(x, str) else x)
        full_document_path = (settings.BASE_DIR+'/media/'+str(document_path))
        with open(full_document_path, "w") as document:
            df.to_csv(document, index=False,na_rep='', line_terminator='\n',sep=';')
        return full_document_path
    
    
    def remove_duplicated_rows(self):
        df=self.df
        document_path=self.document_path
        df = df.drop_duplicates()
        full_document_path = (settings.BASE_DIR+'/media/'+str(document_path))
        with open(full_document_path, "w") as document:
            df.to_csv(document,index=False,na_rep='', line_terminator='\n',sep=';')
        return full_document_path