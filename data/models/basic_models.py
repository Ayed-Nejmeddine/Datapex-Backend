"""Here all Basic models"""
from datetime import datetime

from django.core.validators import FileExtensionValidator
from django.db import models

from django_currentuser.db.models import CurrentUserField
from jsonfield import JSONField

from data.models import ANALYSIS_TRACE_STATES
from data.models import ANALYSIS_TYPES
from data.models import HOMOGENIZATION_TYPES
from data.models import RUNNING_STATE


class Document(models.Model):
    """Document model"""

    document_path = models.FileField(
        blank=False, null=False, validators=[FileExtensionValidator(allowed_extensions=["csv"])]
    )
    owner = CurrentUserField()
    upload_date = models.DateTimeField(default=datetime.now())
    size = models.DecimalField(max_digits=9, decimal_places=3, null=True, blank=True)
    num_col = models.PositiveIntegerField(null=True, blank=True)
    num_row = models.PositiveIntegerField(null=True, blank=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    doc_type = models.CharField(max_length=100, default="csv")
    objects = models.Manager()

    def __str__(self):
        return self.document_path.name


class RegularExp(models.Model):
    """Regular expression model"""

    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=150)
    subcategory = models.CharField(max_length=150)
    expression = models.CharField(max_length=1000)
    objects = models.Manager()

    def __str__(self):
        """
        Override this method to format RegularExp object.'
        """
        return f"{self.id} - {self.subcategory}"


class AnalysisResult(models.Model):
    """Analysis result model"""

    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    result = JSONField()

    class Meta:  # pylint: disable=C0115,R0903
        abstract = True


class SyntacticResult(AnalysisResult):
    """Syntactic Analysis result model"""

    rule = JSONField()
    objects = models.Manager()

    def __str__(self):
        """
        Override this method to format SyntacticResult object.'
        """
        return f"{self.document} - {self.rule}"


class SemanticResult(AnalysisResult):
    """Semantic Analysis result model"""

    rule = JSONField()
    objects = models.Manager()

    def __str__(self):
        """
        Override this method to format SemanticResult object.'
        """
        return f"{self.document} - {self.rule}"

class ProfilageResult(AnalysisResult):
    """Semantic Analysis result model"""

    rule = JSONField()
    objects = models.Manager()

    def __str__(self):
        """
        Override this method to format ProfilageResult object.'
        """
        return f"{self.document} - {self.rule}"
class SemanticData(models.Model):
    """Semantic Analysis data model"""

    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    data = JSONField()
    objects = models.Manager()


class AnalysisTrace(models.Model):
    """Analysis trace model"""

    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    state = models.CharField(max_length=100, choices=ANALYSIS_TRACE_STATES, default=RUNNING_STATE)
    analysis_type = models.CharField(max_length=100, choices=ANALYSIS_TYPES)
    objects = models.Manager()

    def __str__(self):
        """
        Override this method to format AnalysisTrace object.'
        """
        return f"{self.document} - {self.analysis_type}"


class DataDict(models.Model):
    """Data dict model"""

    data_dict = JSONField()
    category = models.CharField(max_length=150)
    objects = models.Manager()


class Link(models.Model):
    """link model"""

    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    first_column = models.CharField(max_length=200)
    second_column = models.CharField(max_length=200)
    relationship = models.CharField(max_length=100)
    objects = models.Manager()


class HomogenizationTrace(models.Model):
    """Homogenization class"""

    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    state = models.CharField(max_length=100, choices=ANALYSIS_TRACE_STATES, default=RUNNING_STATE)
    homogenization_type = models.CharField(max_length=100, choices=HOMOGENIZATION_TYPES)

    def __str__(self):
        """
        Override this method to format HomogenizationTrace object.'
        """
        return f"{self.document} - {self.homogenization_type}"
