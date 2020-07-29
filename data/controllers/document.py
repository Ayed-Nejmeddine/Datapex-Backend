from rest_framework import viewsets, status
from data.models.basic_models import Document
from data.serializers.document_serializer import DocumentSerializer
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from data.services.syntactic import Analyser
from rest_framework.response import Response
from data.models.basic_models import AnalysisTrace
from data.models import BASIC_ANALYSIS, RUNNING_STATE


class DocumentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Document attachments to be viewed or edited.
    """

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_class = (FileUploadParser,)
    permission_classes = (IsAuthenticated, )

    @action(detail=True, methods=['GET'], url_name='launch-syntactic-analysis', url_path='launch-syntactic-analysis')
    def launch_syntactic_analysis(self, request, pk=None):
        """ launch the syntactic analysis."""
        document = self.get_object()
        AnalysisTrace.objects.update_or_create(document=document, analysis_type=BASIC_ANALYSIS,
                                               defaults={'document': document, 'analysis_type': BASIC_ANALYSIS, 'state': RUNNING_STATE})
        analyser = Analyser(document=document)
        analyser.start()
        return Response(status.HTTP_200_OK)
