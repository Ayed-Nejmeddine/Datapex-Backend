"""Here city serializer"""
from cities_light.models import City
from cities_light.models import Country
from rest_framework import serializers


# pylint: disable=R0903
class CountrySerializer(serializers.ModelSerializer):
    """
    Serializer class for Country model.
    """

    class Meta:  # pylint: disable=C0115,R0903
        model = Country
        fields = ("id", "code2", "name", "phone")


# pylint: disable=R0903
class CitySerializer(serializers.ModelSerializer):
    """
    Serializer class for City model.
    """

    country = CountrySerializer()

    class Meta:  # pylint: disable=C0115,R0903
        model = City
        fields = ("id", "display_name", "name", "country")
