from rest_framework import serializers
from .models import News

class NewsSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.company')

    class Meta:
        model = News
        fields = ('owner','title','text','image','place','links','created_at')


class NewsListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.name')

    class Meta:
        model = News
        fields = ('id','owner','title','text','image','place','links','created_at')
