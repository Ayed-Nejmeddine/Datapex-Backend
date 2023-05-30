"""
    Profilage
"""
from data.models import M100_3
from data.models import M100_4
from data.models.basic_models import SyntacticResult
from data.models.basic_models import ProfilageResult
from data.services.profilage.interfaces import ProfilageInterface


class ProfilageAnalyser(ProfilageInterface):
    """contains services for Profilage"""

    def __init__(self, df, document_id, document_path):
        super().__init__()
        self.df = df
        self.document_id = document_id
        self.document_path = document_path

    def detect_null_values(self):
        """return position of null values"""
        df = self.df
        columns = df.columns
        result = [None] * len(columns)
        null_values = SyntacticResult.objects.get(document_id=self.document_id, rule=M100_3).result
        for i in range(len(columns)):
            if null_values[columns[i]]:
                col_null = [
                    (i, j) for j in range(len(df[columns[i]])) if df[columns[i]].isnull().iloc[j]
                ]
                result[i] = col_null
        
        
        # save null values (i,j) in database
        ProfilageResult.objects.update_or_create(
                document_id=self.document_id,
                rule=M100_4,
                defaults={"result": result},
            )
        

    def detect_invalid_values(self):
        """remove duplications"""
        self.df = self.df.drop_duplicates()
