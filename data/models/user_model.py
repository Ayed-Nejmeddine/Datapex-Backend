"""This model represent the user."""
from django.contrib.auth.models import User
from django.db import models

from cities_light.models import City
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from data.models import ENGLISH
from data.models import LANGUAGE_OPTIONS
from data.models.company_model import Company

class Profile(models.Model):
    """
    This model represent the profile of the user.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneNumberField()
    phone_is_verified = models.BooleanField(default=False)
    country = CountryField(null=True, blank=True, default=None)
    _city = models.ForeignKey(City, on_delete=models.DO_NOTHING, blank=False, null=False)
    postalCode = models.IntegerField(null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    occupation = models.CharField(max_length=100, null=True, blank=True)
    photo = models.ImageField(upload_to="profile_pictures", null=True, blank=True, default=None)
    language = models.CharField(max_length=50, choices=LANGUAGE_OPTIONS, default=ENGLISH)
    email_is_verified = models.BooleanField(default=False)

    @property
    def city(self):
        """Redefine city"""
        return self._city.name
