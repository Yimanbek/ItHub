from django.urls import path
from .views import CompanyCreateView,Companies_view,CompanyDetailView
urlpatterns = [
    path('create/',CompanyCreateView.as_view()),
    path('companies/',Companies_view.as_view()),
    path('company/<int:id>/',CompanyDetailView.as_view())
]