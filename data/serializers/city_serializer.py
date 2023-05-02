from rest_framework import serializers
from cities_light.models import City, Country


class CountrySerializer(serializers.ModelSerializer):
    """
    Serializer class for Country model.
    """
    class Meta:  # pylint: disable=C0115
        model = Country
        fields = ('code2', 'phone')


class CitySerializer(serializers.ModelSerializer):
    """
    Serializer class for City model.
    """
    country = CountrySerializer()
    class Meta:  # pylint: disable=C0115
        model = City
        fields = ('id', 'display_name', 'country')



