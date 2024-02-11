from django.urls import path
from .views import RegistrationView,LoginView,DashboardView,activation_view,ResetPasswordView,ResetView,ActivationView,LogoutView

urlpatterns = [
    path('register/',RegistrationView.as_view()),
    path('login/',LoginView.as_view()),
    path('dashboard/',DashboardView.as_view()),
    path('activation/',activation_view),
    path('activate/',ActivationView.as_view()),
    path('reset_password_1/',ResetView.as_view()),
    path('reset_password_2/', ResetPasswordView.as_view()),
    path('logout/', LogoutView.as_view()),
]