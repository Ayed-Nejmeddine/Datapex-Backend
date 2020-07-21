from rest_framework import serializers
from data.models import File
from django.utils.translation import ugettext_lazy as _


class FileSerializer(serializers.ModelSerializer):
    """
    Serializer class for File model.
    """
    def validate_file(self, file):
        """ Validate the extention and the size of the uploaded file. """
        if file.size > 500000000:
            raise serializers.ValidationError(_("The size of the video must be less than 500 Mo !"))
        return file

    class Meta:  # pylint: disable=C0115
        model = File
        fields = ('id', 'file',)
