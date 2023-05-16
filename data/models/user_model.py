"""This model represent the user."""
from django.contrib.auth.models import User
from django.db import models

from allauth.account.models import EmailAddress
from cities_light.models import City
from django_countries.fields import CountryField
from phone_verify.models import SMSVerification
from phonenumber_field.modelfields import PhoneNumberField

from data.models import ENGLISH
from data.models import LANGUAGE_OPTIONS


class Profile(models.Model):
    """
    This model represent the profile of the user.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneNumberField()
    country = CountryField(null=True, blank=True, default=None)
    _city = models.ForeignKey(City, on_delete=models.DO_NOTHING, blank=False, null=False)
    postalCode = models.IntegerField(null=True, blank=True)
    company_name = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100, null=True, blank=True)
    photo = models.ImageField(upload_to="profile_pictures", null=True, blank=True, default=None)
    language = models.CharField(max_length=50, choices=LANGUAGE_OPTIONS, default=ENGLISH)

    @property
    def city(self):
        """Redefine city"""
        return self._city.name

    @property
    def email_is_verified(self):
        """Redefine email_is_verified"""
        email = EmailAddress.objects.get(user=self.user)
        return email and email.verified

    @property
    def phone_is_verified(self):
        """Redefine phone_is_verified"""
        phone = SMSVerification.objects.filter(phone_number=self.phone).order_by("-id").first()
        return phone and phone.is_verified
