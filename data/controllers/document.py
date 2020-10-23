from rest_framework import viewsets, status
from data.models.basic_models import Document
from data.serializers.document_serializer import DocumentSerializer, SemanticResultSerializer
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from data.services.syntactic import Analyser
from rest_framework.response import Response
from data.models.basic_models import AnalysisTrace, SyntacticResult, Link, SemanticResult
from data.models import BASIC_ANALYSIS, RUNNING_STATE
import csv
from django.http import HttpResponse
from data.serializers.link_serializer import LinkSerializer
from data.services.semantic import Analyser as SemanticAnalyser


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
                l = []
                for i in header[2:]:
                    if i not in r.result.keys():
                        l.append('')
                    else:
                        l.append(r.result[i])
                l.insert(0,r.rule['rule'])
                l.insert(1, r.rule['signification'])
                output.append(l)
            writer.writerows(output)
            return response
        if not AnalysisTrace.objects.filter(document=document):
            return Response({"message": "Please launch the syntactic analysis first!"})
        return Response({"message": "The syntactic analysis is still running!"})

    @action(detail=True, methods=['GET'], url_name='get-links-between-columns', url_path='get-links-between-columns')
    def get_links_between_columns(self, request, pk=None):
        """ Get the results of the comparison between the columns """
        document = self.get_object()
        qs = AnalysisTrace.objects.filter(document=document)
        if not qs.filter(state='running') and qs:
            links = Link.objects.filter(document=document)
            return Response(LinkSerializer(links, read_only=True, many=True).data)
        if not AnalysisTrace.objects.filter(document=document):
            return Response({"message": "Please launch the syntactic analysis first!"})
        return Response({"message": "Please wait for the syntactic analysis to complete!"})

    @action(detail=True, methods=['GET'], url_name='launch-semantic-analysis', url_path='launch-semantic-analysis')
    def launch_semantic_analysis(self, request, pk=None):
        """ launch the semantic analysis and get the results."""
        document = self.get_object()
        analyser = SemanticAnalyser(document=document)
        analyser.run()
        results = SemanticResult.objects.filter(document=document)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="semantic-results.csv"'
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
        for r in results:
            l = []
            for i in header[2:]:
                if i not in r.result.keys():
                    l.append('')
                else:
                    l.append(r.result[i])
            l.insert(0,r.rule['rule'])
            l.insert(1, r.rule['signification'])
            output.append(l)
        writer.writerows(output)
        return response
