from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.http import HttpResponseRedirect
from django.urls import reverse
from ithub.tasks import send_comment_notification_tasks
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CreatePostSerializer,IndexSerializer,CommentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema


class StandartPaginational(PageNumberPagination):
    page_size = 50
    page_query_param = 'page'
    def get_paginated_response(self,data):
        return Response({
            'links':{
                'next':self.get_next_link(),
                'previous':self.get_previous_link(),
            },
            'count':self.page.paginator.count,
            'results':data
        })
class IndexView(APIView):
    
    def get(self, request):
        paginator = StandartPaginational()
        posts = Post.objects.all()
        paginated_posts = paginator.paginate_queryset(posts, request)
        serializer = IndexSerializer(instance=paginated_posts, many=True)
        return paginator.get_paginated_response(serializer.data)











class StandartPaginational1(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    def get_paginated_response(self,data):
        return Response({
            'count':self.page.paginator.count,
            'results':data,
            'links':{
                'next':self.get_next_link(),
                'previous':self.get_previous_link(),
            }
        })
    




class PostDetailView(APIView):
    
    def get(self, request, post_id):
        paginator = StandartPaginational1()
        post = get_object_or_404(Post, id=post_id)
        comments = Comment.objects.filter(post=post)
        pagination_comments = paginator.paginate_queryset(comments, request)
        comment_serializer = CommentSerializer(instance=pagination_comments, many=True)
        
        data = {
            'post': IndexSerializer(instance=post).data,
            'comments': paginator.get_paginated_response(comment_serializer.data).data 
        }
        
        return Response(data, status=200)


class CreatePostView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=CreatePostSerializer)
    def post(self, request):
        try:
            serializer = CreatePostSerializer(data=request.data,context={'request': request})
            if serializer.is_valid():
                post = serializer.save()
                if post:
                    return Response({'message': 'Your post is created'})
                else:
                    return Response({'error': 'Failed to save the post'})
            else:
                return Response({'error': serializer.errors})
        except Exception as e:
            return Response({'error': str(e)})
    


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated,)
    @swagger_auto_schema(request_body=CommentSerializer)
    def perform_create(self, serializer):
        post_id = self.kwargs.get('id')  
        post = get_object_or_404(Post, id=post_id)
        validated_data = {**serializer.validated_data, 'post': post}
        serializer.save(author=self.request.user, **validated_data)