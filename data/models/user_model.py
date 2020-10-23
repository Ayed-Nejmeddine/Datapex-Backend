from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField


class Profile(models.Model):
    """
    This model represent the profile of the user.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneNumberField(null=True, blank=True, )
    country = CountryField()
    postalCode = models.IntegerField()
