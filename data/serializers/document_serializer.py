"""Here the document serializer"""
# pylint: disable=E0611
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from data.models.basic_models import Document
from data.models.basic_models import SemanticResult


class DocumentSerializer(serializers.ModelSerializer):
    # pylint: disable=R0903
    """
    Serializer class for Document model.
    """

    def validate_document_path(self, document_path):
        """Validate the extention and the size of the uploaded file."""
        if document_path.size > 500000000:
            raise serializers.ValidationError(_("The size of the file must be less than 500 Mo !"))
        return document_path

    class Meta:  # pylint: disable=C0115,R0903
        model = Document
        fields = (
            "id",
            "name",
            "document_path",
            "size",
            "upload_date",
            "num_col",
            "num_row",
            "doc_type",
        )
        read_only_fields = ("size", "upload_date", "num_col", "num_row", "doc_type")


class SemanticResultSerializer(serializers.ModelSerializer):
    """
    Serializer class for SemanticResult.
    """

    # pylint: disable=R0903
    class Meta:  # pylint: disable=C0115
        model = SemanticResult
        fields = (
            "rule",
            "result",
        )
