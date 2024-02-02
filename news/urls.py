from django.urls import path
from .views import NewsCreateView,NewsDetailView,NewsListView

urlpatterns = [
    path('post/',NewsCreateView.as_view(),name = 'post_news'),
    path('news/<int:id>/', NewsDetailView.as_view(), name='detail_view'),
    path('news/', NewsListView.as_view(), name='news_list')
]