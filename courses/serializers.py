from rest_framework import serializers
from .models import Courses

class CoursesSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Courses
        fields = ('id', 'title', 'description', 'file', 'price', 'owner')