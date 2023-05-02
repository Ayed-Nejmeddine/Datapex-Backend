from django.core.management.base import BaseCommand
from data.models.basic_models import DataDict
import glob
import csv
import os
from data.managers.common_managers import BulkCreateManager


class Command(BaseCommand):
    help = 'Insert the data dictionaries in the database'

    def fill_out_data_dict_model(self):
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
                bulk_mgr.done()

    def handle(self, *args, **options):
        self.fill_out_data_dict_model()
