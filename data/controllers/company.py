from rest_framework import mixins, viewsets
from data.models.company_model import Company
from data.serializers.company_serializer import CompanySerializer
from rest_framework.permissions import IsAuthenticated

class CompanyViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    permission_classes = [
        IsAuthenticated,
    ]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer