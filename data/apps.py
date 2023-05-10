"""Fill DB with regular expressions and data dictionaries"""
import csv
import json
import os
from os import listdir
from os.path import isfile
from os.path import join

from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate
from django.utils import timezone

from background_task.models import Task

from data.models.basic_models import DataDict
from data.models.basic_models import RegularExp


def fill_out_regexp_model(sender, **kwargs):  # pylint: disable=W0613
    """
    fill in the RegularExp table from DDRE file
    """

    file = os.path.join(settings.BASE_DIR, "data", "data_types", "DDRE.csv")
    with open(file, encoding="iso-8859-1") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        next(csv_reader)  # skip
        for row in csv_reader:
            RegularExp.objects.update_or_create(
                category=row[0], subcategory=row[1], expression=row[2]
            )


def fill_out_data_dict_model(sender, **kwargs):  # pylint: disable=W0613
    """
    fill in the data_dict table from files in the "data_dictionaries" directory
    """

    repository = os.path.abspath("data/data_dictionaries")
    files_list = [
        f for f in listdir(repository) if isfile(join(repository, f)) and f.endswith(".csv")
    ]
    nbr = 0
    for f in files_list:
        file = os.path.join(settings.BASE_DIR, "data", "data_dictionaries", f)
        globalJsonArray = []
        jsonArray = []
        with open(file, encoding="iso-8859-1") as f:
            csvReader = csv.DictReader(f, delimiter=";")

            for row, count in enumerate(csvReader):
                jsonArray.append(row)

                if count == 12000:
                    jsonArrayString = json.dumps(jsonArray)
                    globalJsonArray.append(jsonArrayString)
                    jsonArray = []
                    count = 0
            if jsonArray != []:
                jsonArrayString = json.dumps(jsonArray)
                globalJsonArray.append(jsonArrayString)

            for Array in globalJsonArray:
                DataDict.objects.update_or_create(data_dict=Array)
                nbr += 1


def create_tasks(sender, **kwargs):  # pylint: disable=W0613
    """
    Create scheduled periodic task to trace the running threads.
    """

    Task.objects.update_or_create(
        task_name="data.services.trace_threads",
        run_at=timezone.now(),
        repeat=2 * Task.HOURLY,
        task_params="[[], {}]",
    )


class DataConfig(AppConfig):
    """
    Data configuration
    """

    name = "data"

    def ready(self):
        post_migrate.connect(fill_out_regexp_model, sender=self)
        post_migrate.connect(fill_out_data_dict_model, sender=self)
        post_migrate.connect(create_tasks, sender=self)
