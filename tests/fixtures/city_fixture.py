"""Here city fixture."""
import os

from django.conf import settings
from django.core.management import call_command

import pytest


@pytest.fixture(name="_import_city_fixture")
def import_city_fixture(django_db_blocker):
    """
    Load data from file city.json
    """
    with django_db_blocker.unblock():
        call_command(
            "loaddata",
            os.path.join(settings.BASE_DIR, "tests/data/data_cities_light_test/city.json"),
        )
