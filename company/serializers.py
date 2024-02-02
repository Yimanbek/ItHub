from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.email')

    class Meta:
        model = Company
        fields = '__all__'