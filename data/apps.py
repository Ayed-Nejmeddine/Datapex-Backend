from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate
import csv
import os


def fill_out_regexp_model(sender, **kwargs):  # pylint: disable=W0613
    """
    fill in the RegularExp table from DDRE file
    """
    from data.models.models import RegularExp
    file = os.path.join(settings.BASE_DIR, 'data', 'data_types', 'DDRE.csv')
    with open(file, encoding='iso-8859-1') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)  # skip
        for row in csv_reader:
            RegularExp.objects.update_or_create(category=row[0],
                                                subcategory=row[1],
                                                expression=row[2])


class DataConfig(AppConfig):
    name = 'data'

    def ready(self):
        post_migrate.connect(fill_out_regexp_model, sender=self)

