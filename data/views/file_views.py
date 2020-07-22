from rest_framework import viewsets
from data.models.basic_models import File
from data.serializers.file_serializer import FileSerializer
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated


class FileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows File attachments to be viewed or edited.
    """

    queryset = File.objects.all()
    serializer_class = FileSerializer
    parser_class = (FileUploadParser,)
    permission_classes = (IsAuthenticated, )

