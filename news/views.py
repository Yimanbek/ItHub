from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.permissions import IsAuthenticated 
from rest_framework.views import APIView
from .serializers import NewsSerializer
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from .models import News

class NewsCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    
    def get(self, request):
        return render(request, 'post_news.html')

    def post(self, request):
        try:
            if request.user.is_authenticated:
                serializer = NewsSerializer(data=request.data)
                if serializer.is_valid():
                    company = request.user.company 
                    news = serializer.save(owner=company)
                    if news:
                        return redirect('news_list')  # Перенаправление на детальный просмотр новости
                    else:
                        return render(request, 'post_news.html', {'error': 'Data are don\'t save'})
                else:
                    return render(request, 'post_news.html', {'error': 'Your data is not valid'})
            else:
                return render(request, 'post_news.html', {'error': 'User is not authenticated'})
        except Exception as e:
            return render(request, 'post_news.html', {'error': f'An error occurred: {str(e)}'})

class NewsDetailView(APIView):
    def get(self, request, id):
        try:
            news = get_object_or_404(News, id=id)
            return render(request, 'detail_news.html', {'news': news})
        except Exception as e:
            return render(request, 'detail_news.html', {'error': f'An error occurred: {str(e)}'})

class NewsListView(APIView):
    def get(self, request):
        try:
            news_list = News.objects.all()
            return render(request, 'news_list.html', {'news_list': news_list})
        except Exception as e:
            return render(request, 'news_list.html', {'error': f'An error occurred: {str(e)}'})
