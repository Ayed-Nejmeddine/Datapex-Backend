from django.core.management.base import BaseCommand
from collections import defaultdict
from django.apps import apps
from data.models.basic_models import DataDict
import glob
import csv
import os


class BulkCreateManager(object):
    """
    This helper class keeps track of ORM objects to be created for multiple
    model classes, and automatically creates those objects with `bulk_create`
    when the number of objects accumulated for a given model class exceeds
    `chunk_size`.
    Upon completion of the loop that's `add()`ing objects, the developer must
    call `done()` to ensure the final set of objects is created for all models.
    """

    def __init__(self, chunk_size=200):
        self._create_queues = defaultdict(list)
        self.chunk_size = chunk_size

    def _commit(self, model_class):
        model_key = model_class._meta.label
        model_class.objects.bulk_create(self._create_queues[model_key])
        self._create_queues[model_key] = []

    def add(self, obj):
        """
        Add an object to the queue to be created, and call bulk_create if we
        have enough objs.
        """
        model_class = type(obj)
        model_key = model_class._meta.label
        self._create_queues[model_key].append(obj)
        if len(self._create_queues[model_key]) >= self.chunk_size:
            self._commit(model_class)

    def done(self):
        """
        Always call this upon completion to make sure the final partial chunk
        is saved.
        """
        for model_name, objs in self._create_queues.items():
            if len(objs) > 0:
                self._commit(apps.get_model(model_name))


class Command(BaseCommand):
    help = 'Insert the data dictionaries in the database'

    def fill_out_data_dict_model(self):  # pylint: disable=W0613
        """
        fill in the DataDict table
        """
        bulk_mgr = BulkCreateManager(chunk_size=2000)
        os.chdir("data/data_dictionaries")
        for file in glob.glob("*.csv"):
            with open(file, encoding='windows-1252') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=';')
                first_row = next(csv_reader)
                for row in csv_reader:
                    bulk_mgr.add(DataDict(data_dict={first_row[i]: row[i] for i in range(len(first_row))}))

    def handle(self, *args, **options):
        self.fill_out_data_dict_model()
