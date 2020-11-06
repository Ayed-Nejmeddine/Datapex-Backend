from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from data.models import LANGUAGE_OPTIONS, ENGLISH
from cities_light.models import City


class Profile(models.Model):
    """
    This model represent the profile of the user.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneNumberField()
    phone_is_verified = models.BooleanField(default=False)
    country = CountryField(null=True, blank=True, default=None)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING, blank=False, null=False)
    postalCode = models.IntegerField(null=True, blank=True)
    company_name = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100,null=True, blank=True)
    photo = models.ImageField(upload_to='profile_pictures', null=True, blank=True, default=None)
    language = models.CharField(max_length=50, choices=LANGUAGE_OPTIONS, default=ENGLISH)
    email_is_verified = models.BooleanField(default=False)
