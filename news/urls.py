from django.urls import path
from .views import NewsCreateView,NewsDetailView,NewsListView

urlpatterns = [
    path('post/',NewsCreateView.as_view()),
    path('news_detail/<int:id>/', NewsDetailView.as_view()),
    path('news/', NewsListView.as_view())
]