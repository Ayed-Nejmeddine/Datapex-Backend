from rest_framework import viewsets
from data.models import File
from data.serializers import FileSerializer
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework import status


class FileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows File attachments to be viewed or edited.
    """

    queryset = File.objects.all()
    serializer_class = FileSerializer
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):

        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid(raise_exception=True):
            file_serializer.save()
        return Response(file_serializer.data, status=status.HTTP_201_CREATED)
