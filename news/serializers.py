from rest_framework import serializers
from .models import News

class NewsSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.company')

    class Meta:
        model = News
        fields = ('owner','title','text','image','place','links','created_at')
