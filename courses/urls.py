from django.urls import path
from .views import CoursesCreateView, CoursesDetailView, CoursesListView

urlpatterns = [
    path('create/', CoursesCreateView.as_view()),
    path('course/<int:id>/', CoursesDetailView.as_view()),
    path('courses/', CoursesListView.as_view()),
]