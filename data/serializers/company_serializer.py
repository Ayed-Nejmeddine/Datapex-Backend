from rest_framework import serializers
from data.models.company_model import Company

class CompanySerializer(serializers.ModelSerializer):
    """
    Serializer class for Company model.
    """
    
    def validate_siret(self, siret):
        if not siret.isdigit() or len(siret) != 14:
            raise serializers.ValidationError("Invalid SIRET number")

        return siret
    class Meta:
        model = Company
        fields = ('id', 'name', 'address', 'siret')