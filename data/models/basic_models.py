from django.db import models
from django.core.validators import FileExtensionValidator
from jsonfield import JSONField
from data.models import ANALYSIS_TRACE_STATES, RUNNING_STATE, ANALYSIS_TYPES
from django_currentuser.db.models import CurrentUserField
from datetime import datetime


class Document(models.Model):
    document_path = models.FileField(blank=False, null=False, validators=[FileExtensionValidator(allowed_extensions=['csv'])])
    owner = CurrentUserField()
    upload_date = models.DateTimeField(default=datetime.now())
    size = models.DecimalField(max_digits=9, decimal_places=3, null=True, blank=True)
    num_col = models.PositiveIntegerField(null=True, blank=True)
    num_row = models.PositiveIntegerField(null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    doc_type = models.CharField(max_length=100, default='csv')

    objects = models.Manager()

    def __str__(self):
        return self.document_path.name


class RegularExp(models.Model):
    category = models.CharField(max_length=150)
    subcategory = models.CharField(max_length=150)
    expression = models.CharField(max_length=1000)

    objects = models.Manager()

    def __str__(self):
        """
        Override this method to format RegularExp object.'
        """
        return f'{self.id} - {self.subcategory}'


class AnalysisResult(models.Model):
    document = models.ForeignKey(Document, on_delete=models.DO_NOTHING)
    result = JSONField()

    class Meta:  # pylint: disable=C0115
        abstract = True


class SyntacticResult(AnalysisResult):
    rule = JSONField()

    objects = models.Manager()

    def __str__(self):
        """
        Override this method to format SyntacticResult object.'
        """
        return f'{self.document} - {self.rule}'


class SemanticResult(AnalysisResult):
    rule = JSONField()

    objects = models.Manager()

    def __str__(self):
        """
        Override this method to format SemanticResult object.'
        """
        return f'{self.document} - {self.rule}'


class SemanticData(models.Model):
    document = models.ForeignKey(Document, on_delete=models.DO_NOTHING)
    data = JSONField()
    objects = models.Manager()


class AnalysisTrace(models.Model):
    document = models.ForeignKey(Document, on_delete=models.DO_NOTHING)
    state = models.CharField(max_length=100, choices=ANALYSIS_TRACE_STATES, default=RUNNING_STATE)
    analysis_type = models.CharField(max_length=100, choices=ANALYSIS_TYPES)

    objects = models.Manager()

    def __str__(self):
        """
        Override this method to format AnalysisTrace object.'
        """
        return f'{self.document} - {self.analysis_type}'


class DataDict(models.Model):
    data_dict = JSONField()
    objects = models.Manager()


class Link(models.Model):
    document = models.ForeignKey(Document, on_delete=models.DO_NOTHING)
    first_column = models.CharField(max_length=200)
    second_column = models.CharField(max_length=200)
    relationship = models.CharField(max_length=100)

    objects = models.Manager()

