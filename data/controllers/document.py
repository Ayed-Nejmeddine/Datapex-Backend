"""Here all document APIs."""
import csv
import json

from django.db.models import Q
from django.http import HttpResponse

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from data.models import BASIC_ANALYSIS
from data.models import RUNNING_STATE
from data.models.basic_models import AnalysisTrace
from data.models.basic_models import Document
from data.models.basic_models import Link
from data.models.basic_models import SemanticResult
from data.models.basic_models import SyntacticResult
from data.serializers.document_serializer import DocumentSerializer
from data.serializers.link_serializer import LinkSerializer
from data.services.semantic import Analyser as SemanticAnalyser
from data.services.syntactic import Analyser


class DocumentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Document attachments to be viewed or edited.
    """

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_class = (FileUploadParser,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Get all documents according to current user.
        :return: list of documents.
        """
        objects = Document.objects.filter(owner=self.request.user).order_by("-upload_date")
        return objects

    @action(
        detail=True,
        methods=["GET"],
        url_name="launch-syntactic-analysis",
        url_path="launch-syntactic-analysis",
    )
    def launch_syntactic_analysis(self, request, pk=None):
        """launch the syntactic analysis."""
        document = self.get_object()
        AnalysisTrace.objects.update_or_create(
            document=document,
            analysis_type=BASIC_ANALYSIS,
            defaults={
                "document": document,
                "analysis_type": BASIC_ANALYSIS,
                "state": RUNNING_STATE,
            },
        )
        analyser = Analyser(document=document)
        analyser.start()
        return Response(
            {"message": "The syntactic analysis has been launched."}, status.HTTP_200_OK
        )

    @action(
        detail=True,
        methods=["GET"],
        url_name="get-syntactic-analysis-results",
        url_path="get-syntactic-analysis-results",
    )
    def get_syntactic_results(self, request, pk=None):
        """Get the syntactic analysis results."""
        document = self.get_object()
        qs = AnalysisTrace.objects.filter(document=document)
        if not qs.filter(state="running") and qs:
            response = HttpResponse(content_type="application/json")
            # JSON Data
            output = {}
            with document.document_path.open("r") as f:
                reader = csv.reader(f, delimiter=";")
                header = next(reader)
            results = SyntacticResult.objects.filter(document=document)
            for r in results:
                output[r.rule["rule"]] = {}
                res_dict = {}
                for i in header:
                    if i not in r.result.keys():  # noqa: SIM401
                        res_dict = r.result
                    else:
                        res_dict[i] = r.result[i]
                res_dict["Signification"] = r.rule["signification"]
                output[r.rule["rule"]] = res_dict

            # Write JSON to response
            json.dump(output, response, ensure_ascii=False, indent=4)

            return response
        if not AnalysisTrace.objects.filter(document=document):
            return Response({"message": "Please launch the syntactic analysis first!"})
        return Response({"message": "The syntactic analysis is still running!"})

    @action(
        detail=True,
        methods=["GET"],
        url_name="get-links-between-columns",
        url_path="get-links-between-columns",
    )
    def get_links_between_columns(self, request, pk=None):
        """Get the results of the comparison between the columns"""
        document = self.get_object()
        qs = AnalysisTrace.objects.filter(document=document)
        if not qs.filter(state="running") and qs:
            links = Link.objects.filter(document=document)
            return Response(LinkSerializer(links, read_only=True, many=True).data)
        if not AnalysisTrace.objects.filter(document=document):
            return Response({"message": "Please launch the syntactic analysis first!"})
        return Response({"message": "Please wait for the syntactic analysis to complete!"})

    @action(
        detail=True,
        methods=["GET"],
        url_name="launch-semantic-analysis",
        url_path="launch-semantic-analysis",
    )
    def launch_semantic_analysis(self, request, pk=None):
        """launch the semantic analysis and get the results."""
        document = self.get_object()
        try:
            SemanticAnalyser(document=document).run()
        except Exception as e:
            return Response({"message": f"Run the Syntactic analysis first, error:{e}"})
        results = SemanticResult.objects.filter(document=document)
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="semantic-results.csv"'
        writer = csv.writer(response)
        # Header
        with document.document_path.open("r") as f:
            reader = csv.reader(f)
            header = next(reader)
            header.insert(0, "Rule")
            header.insert(1, "Signification")
            writer.writerow(header)

        # CSV Data
        output = []
        for r in results:
            liste = []
            for i in header[2:]:
                if i not in r.result.keys():
                    liste.append("")
                else:
                    liste.append(r.result[i])
            liste.insert(0, r.rule["rule"])
            liste.insert(1, r.rule["signification"])
            output.append(liste)
        writer.writerows(output)
        return response

    @action(
        detail=False,
        methods=["GET"],
        url_name="get-latest-treated-document",
        url_path="get-latest-treated-document",
    )
    def get_latest_treated_document(self, request, pk=None):
        """Get the latest document that as treated syntactically"""
        documents = request.user.document_set.filter(
            ~Q(analysistrace__state=RUNNING_STATE)
        ).distinct()
        qs = AnalysisTrace.objects.filter(document__owner=request.user, state="finished")
        if not qs:
            return Response({"message": "No document has yet been analyzed"})
        latest_doc = documents.latest("upload_date")
        return Response(DocumentSerializer(latest_doc, read_only=True).data)
