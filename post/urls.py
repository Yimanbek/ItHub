from django.urls import path, include
from . import views




urlpatterns = [
    path('', views.IndexView.as_view()),
    path('post/<int:post_id>/', views.PostDetailView.as_view()),
    path('create_post/', views.CreatePostView.as_view()),
    path('post/<int:id>/create_comment/', views.CommentCreateView.as_view()),
    
]
