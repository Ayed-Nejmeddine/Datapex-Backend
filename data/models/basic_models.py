from django.db import models
from django.core.validators import FileExtensionValidator


class File(models.Model):
    file = models.FileField(blank=False, null=False, validators=[FileExtensionValidator(allowed_extensions=['csv'])])

    def __str__(self):
        return self.file.name


class RegularExp(models.Model):
    category = models.CharField(max_length=150)
    subcategory = models.CharField(max_length=150)
    expression = models.CharField(max_length=1000)

    def __str__(self):
        """
        Override this method to format RegularExp object.'
        """
        return f'{self.id} - {self.subcategory}'
