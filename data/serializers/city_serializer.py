from rest_framework import serializers
from cities_light.models import City, Country


class CitySerializer(serializers.ModelSerializer):
    """
    Serializer class for City model.
    """
    class Meta:  # pylint: disable=C0115
        model = City
        fields = ('id', 'display_name')


class CountrySerializer(serializers.ModelSerializer):
    """
    Serializer class for Country model.
    """
    class Meta:  # pylint: disable=C0115
        model = Country
        fields = ('id', 'name')
