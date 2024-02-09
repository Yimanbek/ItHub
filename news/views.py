from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.views import APIView
from .serializers import NewsSerializer,NewsListSerializer
from django.urls import reverse
from rest_framework.response import Response
from .models import News
from account.permissions import IsAuthor,IsAuthorOrAdmin
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema 



class StandartPaginational(PageNumberPagination):
    page_size = 20
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





class NewsCreateView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=NewsSerializer)
    def post(self, request):  
        try:
            if request.user.is_authenticated:
                serializer = NewsSerializer(data=request.data)
                if serializer.is_valid():
                    company = request.user.company 
                    news = serializer.save(owner=company)
                    if news:
                        return Response({'message':'Your news is save and successfully'})
                    else:
                        return Response({'error': 'Data are don\'t save'})
                else:
                    return Response({'error': 'Your data is not valid'})
            else:
                return Response({'error': 'User is not authenticated'})
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'})



class NewsDetailView(APIView):
    def get(self, request, id):
        try:
            news = get_object_or_404(News, id=id)
            serializer = NewsListSerializer(news)
            return Response({'news': serializer.data, 'message': 'Successfully retrieved'})
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'})
        
    def delete(self,request,id):
        try:
            news = get_object_or_404(News,id=id)
            if request.user == news.owner.owner:
                news.delete()
                return Response({'message':'Your news is delete!'})
            return Response({'error':'You don\t have a permissions for delete'})
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'})

class NewsListView(APIView):


    def get(self, request):
        paginator = StandartPaginational()
        try:
            news_list = News.objects.all()
            paginations_news = paginator.paginate_queryset(news_list,request)
            serializer = NewsListSerializer(paginations_news, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'})
