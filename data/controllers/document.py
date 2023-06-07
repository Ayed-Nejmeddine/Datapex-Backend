"""Here all document APIs."""
import csv
import json

from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from data.models import BASIC_ANALYSIS
from data.models import M102_25
from data.models import M103_30
from data.models import M103_31
from data.models import M104_5
from data.models import M104_6
from data.models import RUNNING_STATE
from data.models.basic_models import AnalysisTrace
from data.models.basic_models import Document
from data.models.basic_models import Link
from data.models.basic_models import ProfilageResult
from data.models.basic_models import SemanticResult
from data.models.basic_models import SyntacticResult
from data.serializers.document_serializer import DocumentSerializer
from data.serializers.link_serializer import LinkSerializer
from data.services.homgenization import Homogenization
from data.services.profilage import Profilage
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
        
        analyser.join()
        return Response(
            {"message": ["The syntactic analysis has been launched."]}, status.HTTP_200_OK
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
            return Response(
                {"message": ["Please launch the syntactic analysis first!"]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"message": ["The syntactic analysis is still running!"]},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        detail=True,
        methods=["GET"],
        url_name="get-global_syntactic-analysis-results",
        url_path="get-global_syntactic-analysis-results",
    )
    # pylint: disable=R0912
    # pylint: disable=R0914
    def get_global_syntactic_results(self, request, pk=None):
        """Get the global_syntactic analysis results."""
        document = self.get_object()
        qs = AnalysisTrace.objects.filter(document=document)
        # pylint: disable=R1702
        if not qs.filter(state="running") and qs:
            response = HttpResponse(content_type="application/json")
            # JSON Data
            base_rule = [
                "Total",
                "M100 [3]",
                "M101 [4]",
                "M114 [17]",
                "M102 [5]",
                "M103 [6]",
                "M103 [7]",
                "M112 [15]",
                "M104 [7]",
                "M111 [14]",
                "M130 [1]",
                "M130 [2]",
                "M130 [3]",
                "M113 [16]",
                "M115 [18]",
                "M103 [8]",
                "M104 [20]",
                "M104 [21]",
            ]
            output = {}
            with document.document_path.open("r") as f:
                reader = csv.reader(f, delimiter=";")
                header = next(reader)
            sumText = 0
            sumDate = 0
            sumNum = 0
            sumBool = 0
            sumMixt = 0
            for r in SyntacticResult.objects.filter(document=document):
                if r.rule["rule"] in base_rule:
                    output[r.rule["rule"]] = {}
                    res_dict = {}
                    somme = 0
                    for i in header:
                        if i not in r.result.keys():  # noqa: SIM401
                            res_dict = r.result
                        else:
                            if isinstance(r.result[i], dict):
                                if r.result[i]["string"] == 100.0:
                                    sumText += 1
                                elif r.result[i]["number"] == 100.0:
                                    sumNum += 1
                                elif r.result[i]["boolean"] == 100.0:
                                    sumBool += 1
                                elif r.result[i]["date"] == 100.0:
                                    sumDate += 1
                                else:
                                    sumMixt += 1
                                res = {
                                    "string": sumText,
                                    "number": sumNum,
                                    "boolean": sumBool,
                                    "date": sumDate,
                                    "mixte": sumMixt,
                                }
                                res_dict = res
                            else:
                                somme += r.result[i]
                                res_dict["sum"] = somme
                    res_dict["Signification"] = r.rule["signification"]

                    output[r.rule["rule"]] = res_dict

            # Write JSON to response
            json.dump(output, response, ensure_ascii=False, indent=4)

            return response
        if not AnalysisTrace.objects.filter(document=document):
            return Response(
                {"message": ["Please launch the syntactic analysis first!"]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"message": ["The syntactic analysis is still running!"]},
            status=status.HTTP_400_BAD_REQUEST,
        )

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
            return Response({"message": ["Please launch the syntactic analysis first!"]})
        return Response({"message": ["Please wait for the syntactic analysis to complete!"]})

    @action(
        detail=True,
        methods=["GET"],
        url_name="launch-semantic-analysis",
        url_path="launch-semantic-analysis",
    )
    def launch_semantic_analysis(self, request, pk=None):
        """launch the semantic analysis and get the results."""
        document = self.get_object()

        if AnalysisTrace.objects.filter(document=document, state="running"):
            raise ValidationError({"message": ["the syntactic analysis still running!"]})
        if not AnalysisTrace.objects.filter(document=document, state="finished"):
            raise ValidationError({"message": ["Please launch the syntactic analysis first!"]})
        try:
            SemanticAnalyser(document=document).run()
            return Response(
                {"message": ["The semantic analysis has been launched."]}, status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"message": [f"Run the Syntactic analysis first, error:{e}"]})

    @action(
        detail=True,
        methods=["GET"],
        url_name="get-semantic-analysis-results",
        url_path="get-semantic-analysis-results",
    )
    def get_semantic_results(self, request, pk=None):
        """Get the semantic analysis results."""
        document = self.get_object()
        if not SemanticResult.objects.filter(document=document):
            return Response(
                {"message": ["Please launch the semantic analysis first!"]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        categories_res = SemanticResult.objects.get(document=document, rule=M102_25)
        valid_values_dom_cat = SemanticResult.objects.get(document=document, rule=M103_30)
        invalid_values_dom_cat = SemanticResult.objects.get(document=document, rule=M104_5)
        valid_values_dom_sub_cat = SemanticResult.objects.get(document=document, rule=M103_31)
        invalid_values_dom_sub_cat = SemanticResult.objects.get(document=document, rule=M104_6)

        output = {}
        columns = list(categories_res.result.keys())
        categories = {}

        for col in categories_res.result:
            if categories_res.result[col] == "NON APPLICABLE":
                pass
            else:
                for cat in categories_res.result[col]:
                    if cat != "no-match":
                        if cat not in categories:
                            categories[cat] = [
                                {colum: 0} for colum in columns
                            ]  # WE MUST KEEP THE SAME ORDER OF COLUMNS TO HAVE AN EXACT RESULT IN THE FRONT
                            categories[cat][columns.index(col)] = {
                                col: categories_res.result[col][cat]
                            }  # lEST4S AFFECT THE CORRESPONDING VALUE TO THE RIGHT COLUMN
                        else:
                            categories[cat][columns.index(col)] = {
                                col: categories_res.result[col][cat]
                            }

        categories_result = {
            "Rule": categories_res.rule["rule"],
            "Signification": categories_res.rule["signification"],
            "Result": categories,
        }
        valid_values_dom_cat = {
            "Rule": valid_values_dom_cat.rule["rule"],
            "Signification": valid_values_dom_cat.rule["signification"],
            "Result": valid_values_dom_cat.result,
        }
        invalid_values_dom_cat = {
            "Rule": invalid_values_dom_cat.rule["rule"],
            "Signification": invalid_values_dom_cat.rule["signification"],
            "Result": invalid_values_dom_cat.result,
        }
        valid_values_dom_sub_cat = {
            "Rule": valid_values_dom_sub_cat.rule["rule"],
            "Signification": valid_values_dom_sub_cat.rule["signification"],
            "Result": valid_values_dom_sub_cat.result,
        }
        invalid_values_dom_sub_cat = {
            "Rule": invalid_values_dom_sub_cat.rule["rule"],
            "Signification": invalid_values_dom_sub_cat.rule["signification"],
            "Result": invalid_values_dom_sub_cat.result,
        }
        output[1] = categories_result
        output[2] = valid_values_dom_cat
        output[3] = invalid_values_dom_cat
        output[4] = valid_values_dom_sub_cat
        output[5] = invalid_values_dom_sub_cat
        return JsonResponse(output)

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
            return Response({"message": ["No document has yet been analyzed"]})
        latest_doc = documents.latest("upload_date")
        return Response(DocumentSerializer(latest_doc, read_only=True).data)

    @action(
        detail=True,
        methods=["POST"],
        url_name="launch-document-cleaning",
        url_path="launch-document-cleaning",
    )
    def launch_document_cleaning(self, request, pk=None):
        """Remove spaces and duplicated rows in the document"""
        document = self.get_object()

        if not (
            AnalysisTrace.objects.filter(document=document, state="running")
            or AnalysisTrace.objects.filter(document=document, state="finished")
        ):
            return Response(
                {"message": ["Please launch the syntactic analysis first!"]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            Homogenization(document=document).run()
            return Response(
                {"message": ["The document is cleanned successfully."]}, status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"message": [f"The document cleaning failed, error:{e}"]})

    @action(
        detail=True,
        methods=["GET"],
        url_name="launch-document-profilage",
        url_path="launch-document-profilage",
    )
    def launch_document_profilage(self, request, pk=None):
        """Returs null and invalid values"""
        document = self.get_object()

        if not (
            AnalysisTrace.objects.filter(document=document, state="running")
            or AnalysisTrace.objects.filter(document=document, state="finished")
        ):
            return Response(
                {"message": ["Please launch the syntactic analysis first!"]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            Profilage(document=document).run()
            return Response(
                {"message": ["document profilage is launched successfully ."]}, status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"message": [f"The document profilage failed, error:{e}"]})

    @action(
        detail=True,
        methods=["GET"],
        url_name="get-profilage-results",
        url_path="get-profilage-results",
    )
    def get_profilage_results(self, request, pk=None):
        """Get the profilage results."""
        document = self.get_object()
        response = HttpResponse(content_type="application/json")
        if not {ProfilageResult.objects.filter(document=document)}:
            return Response(
                {"message": ["Please launch the profilage first!"]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        output = {}
        results = ProfilageResult.objects.filter(document=document)
        for r in results:
            output[r.rule["rule"]] = {}
            res_dict = {"result": r.result}
            output[r.rule["rule"]] = res_dict
        json.dump(output, response, ensure_ascii=False, indent=4)
        return response
