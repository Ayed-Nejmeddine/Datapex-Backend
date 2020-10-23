from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate
import csv
import os


def fill_out_regexp_model(sender, **kwargs):  # pylint: disable=W0613
    """
    fill in the RegularExp table from DDRE file
    """
    from data.models.basic_models import RegularExp
    file = os.path.join(settings.BASE_DIR, 'data', 'data_types', 'DDRE.csv')
    with open(file, encoding='iso-8859-1') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)  # skip
        for row in csv_reader:
            RegularExp.objects.update_or_create(category=row[0],
                                                subcategory=row[1],
                                                expression=row[2])


def create_tasks(sender, **kwargs):  # pylint: disable=W0613
    """
    Create scheduled periodic task to trace the running threads.
    """
    from background_task.models import Task
    from django.utils import timezone
    Task.objects.update_or_create(task_name='data.services.trace_threads',
                                  run_at=timezone.now(),
                                  repeat=2 * Task.HOURLY,
                                  task_params='[[], {}]')


class DataConfig(AppConfig):
    name = 'data'

    def ready(self):
        import data.signals
        post_migrate.connect(fill_out_regexp_model, sender=self)
        post_migrate.connect(create_tasks, sender=self)
