from rest_framework import serializers
from .models import Post,Comment

class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'content', 'created_at')

    def create(self, validated_data):
        request = self.context.get('request')

        if request:
            user = request.user

            validated_data['author'] = user


        post = super(CreatePostSerializer, self).create(validated_data)

        return post

class IndexSerializer(serializers.ModelSerializer):
      

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    post = serializers.ReadOnlyField(source='post.title')

    class Meta:
        model = Comment
        fields = ['author', 'post', 'content','created_at']




