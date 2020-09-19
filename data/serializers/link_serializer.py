from rest_framework import serializers
from data.models.basic_models import Link


class LinkSerializer(serializers.ModelSerializer):
    """
    Serializer class for Link model.
    """
    class Meta:  # pylint: disable=C0115
        model = Link
        fields = ('first_column', 'relationship', 'second_column')