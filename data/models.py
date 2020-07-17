from django.db import models
from django.core.validators import FileExtensionValidator


class File(models.Model):
    file = models.FileField(blank=False, null=False, validators=[FileExtensionValidator(allowed_extensions=['csv'])])

    def __str__(self):
        return self.file.name
