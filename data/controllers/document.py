from rest_framework import viewsets, status
from data.models.basic_models import Document
from data.serializers.document_serializer import DocumentSerializer
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from data.services.syntactic import Analyser
from rest_framework.response import Response
from data.models.basic_models import AnalysisTrace, SyntacticResult
from data.models import BASIC_ANALYSIS, RUNNING_STATE
import csv
from django.http import HttpResponse


class DocumentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Document attachments to be viewed or edited.
    """

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_class = (FileUploadParser,)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """
        Get all documents according to current user.
        :return: list of documents.
        """
        objects = Document.objects.filter(owner=self.request.user)
        return objects

    @action(detail=True, methods=['GET'], url_name='launch-syntactic-analysis', url_path='launch-syntactic-analysis')
    def launch_syntactic_analysis(self, request, pk=None):
        """ launch the syntactic analysis."""
        document = self.get_object()
        AnalysisTrace.objects.update_or_create(document=document, analysis_type=BASIC_ANALYSIS,
                                               defaults={'document': document, 'analysis_type': BASIC_ANALYSIS, 'state': RUNNING_STATE})
        analyser = Analyser(document=document)
        analyser.start()
        return Response({"message": "The syntactic analysis has been launched."}, status.HTTP_200_OK)

    @action(detail=True, methods=['GET'], url_name='get-syntactic-analysis-results', url_path='get-syntactic-analysis-results')
    def get_syntactic_results(self, request, pk=None):
        """ Get the syntactic analysis results. """
        document = self.get_object()
        qs = AnalysisTrace.objects.filter(document=document)
        if not qs.filter(state='running') and qs:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="syntactic-results.csv"'
            writer = csv.writer(response)
            # Header
            with document.document_path.open('r') as f:
                reader = csv.reader(f)
                header = next(reader)
                header.insert(0, 'Rule')
                header.insert(1, 'Signification')
                writer.writerow(header)

            # CSV Data
            output = []
            results = SyntacticResult.objects.filter(document=document)
            for r in results:
                l = list(r.result.values())
                l.insert(0,r.rule['rule'])
                l.insert(1, r.rule['signification'])
                # output.append(r.rule)
                output.append(l)
            writer.writerows(output)
            return response
        if not AnalysisTrace.objects.filter(document=document):
            return Response({"message": "Please launch the syntactic analysis first!"})
        return Response({"message": "The syntactic analysis is still running!"})
