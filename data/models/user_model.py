from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField


class Profile(models.Model):
    """
    This model represent the profile of the user.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneNumberField()
    phone_is_verified = models.BooleanField(default=False)
    country = CountryField(null=True, blank=True, default=None)
    postalCode = models.IntegerField(null=True, blank=True)
    company_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='profile_pictures', null=True, blank=True, default=None)
