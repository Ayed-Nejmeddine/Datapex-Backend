from rest_framework import viewsets
from data.serializers.city_serializer import CitySerializer, CountrySerializer
from cities_light.models import City, Country
from django_filters import rest_framework as filters


class CityFilter(filters.FilterSet):
    class Meta:
        model = City
        fields = ['name']


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows cities to be viewed.
    """

    permission_classes = ()
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = [filters.DjangoFilterBackend]
    filter_class = CityFilter


class CountryFilter(filters.FilterSet):
    class Meta:
        model = Country
        fields = ['name']


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows countries to be viewed.
    """
    permission_classes = ()
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_backends = [filters.DjangoFilterBackend]
    filter_class = CountryFilter
