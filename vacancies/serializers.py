from .models import Vacancies
from rest_framework import serializers

class VacanciesSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.user.company.name')

    class Meta:
        model = Vacancies
        fields = ('owner','title','description','requirement','schedule','salary')









class VacanciesDetailSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.name')

    class Meta:
        model = Vacancies
        fields = ['owner', 'title','description','requirement','schedule','salary']

class VacanciesListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.name')

    class Meta:
        model = Vacancies
        fields = ('id','owner','title','description','requirement','schedule','salary')
