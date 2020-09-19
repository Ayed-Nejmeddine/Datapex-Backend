from data.services.semantic.interfaces import SemanticInterface


class SemanticAnalyser(SemanticInterface):
    """ contains services for SemanticInterface """
    def __init__(self, df, document_id):
        super().__init__()
        self.df = df
        self.document_id = document_id
