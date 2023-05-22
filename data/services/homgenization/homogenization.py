"""
    Homogenization
"""
from django.conf import settings

from data.models import M112
from data.models import M113
from data.models import M114
from data.models import M115
from data.models import M116
from data.models import M117
from data.models import M118
from data.models import M119
from data.models import M120
from data.models import M121
from data.models.basic_models import SyntacticResult
from data.services.homgenization.interfaces import HomogenizationInterface
from data.services.homgenization.utils import to_date


class HomogenizationAnalyser(HomogenizationInterface):
    """contains services for Homogenization"""

    def __init__(self, df, document_id, document_path):
        super().__init__()
        self.df = df
        self.document_id = document_id
        self.document_path = document_path

    def remove_extra_spaces(self):
        """remove extra spaces for every value"""
        self.df = self.df.applymap(lambda x: " ".join(x.split()) if isinstance(x, str) else x)

    def remove_duplicated_rows(self):
        """remove duplications"""
        self.df = self.df.drop_duplicates()

    def _get_db_result(self, document_id, rule):
        """get syntactic result from db"""
        return SyntacticResult.objects.get(document=document_id, rule=rule)

    def standardisation_date(self):
        """format the dates to the format of the dominant format of the dates in this column"""
        document_id = self.document_id
        date_formats = [
            "%m %d %Y",
            "%m %d %y",
            "%d %b %Y",
            "%d/%m/%Y",
            "%H:%M:%S",
            "%Y-%m-%d",
            "%m/%d/%Y %H:%M",
            "%m/%d/%Y %H:%M:%S",
            "%B",
            "%A",
        ]
        rules = [M112, M113, M114, M115, M116, M117, M118, M119, M120, M121]
        date_result = [self._get_db_result(document_id, rule) for rule in rules]
        columns = list(date_result[0].result.keys())
        for col in columns:
            format_values = [i.result[col] for i in date_result]
            dominant_value = max(format_values)
            dominant_format = date_formats[format_values.index(dominant_value)]
            self.df[col] = (
                self.df[col].fillna("").apply(to_date, dominant_date_format=dominant_format)
            )

    def cleaning_document(self):
        """save changes to the new file"""
        df = self.df
        document_path = self.document_path
        full_document_path = settings.BASE_DIR + "/media/" + str(document_path)
        with open(full_document_path, "w") as document:
            df.to_csv(document, index=False, na_rep="", line_terminator="\n", sep=";")
        return full_document_path
