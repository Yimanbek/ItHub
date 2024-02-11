from django.shortcuts import render, redirect
from django.views import View
from .serializers import RegistrationSerializer, ActivationSerializer, ResetPasswordSerializer
from rest_framework import status
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, get_object_or_404, ListAPIView
from django.contrib.auth import get_user_model, authenticate, login, logout
from rest_framework import permissions
from ithub.tasks import send_confirmation_email_task, send_confirmation_password_task
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib import messages
from rest_framework.authtoken.views import ObtainAuthToken
from .models import CustomUser
from rest_framework.authentication import TokenAuthentication



from drf_yasg.utils import swagger_auto_schema 

User = get_user_model()

class RegistrationView(APIView):
    @swagger_auto_schema(request_body=RegistrationSerializer)
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                try:
                    send_confirmation_email_task(user.email, user.activation_code)
                    return Response({'message': 'Registration successful, confirmation email sent'})
                except:
                    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ActivationView(GenericAPIView):
    serializer_class = ActivationSerializer

    def get(self, request):
        code = request.GET.get('u')
        user = get_object_or_404(User, activation_code=code)
        user.is_active = True
        user.save()
        return Response({'message': 'Activation successful'})
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Activation successful'})
    
def activation_view(request):
    return render(request, 'activation.html')

class DashboardView(View):

    def post(self, request):
        action = request.POST.get('action', None)

        if action == 'login':
            return Response({'message': 'Redirecting to login'})
        elif action == 'register':
            return Response({'message': 'Redirecting to registration'})
        elif action == 'home':
            return Response({'message': 'Redirecting to home'})
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            return Response({'error': 'Email and Password are required!'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            token, create = Token.objects.get_or_create(user=user)

            if token:
                return Response({'message': 'Login successful'})
            else:
                return Response({'error': 'Login failed'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            messages.error(request, 'Invalid email or password')
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)


class ResetView(APIView):

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Please provide an email address'}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(CustomUser, email=email)
        password_change_code = user.create_number_code()
        user.password_change_code = password_change_code
        user.save()
        send_confirmation_password_task(user.email, password_change_code)

        return Response({'message': 'Password reset email sent'})

class ResetPasswordView(APIView):
    @swagger_auto_schema(request_body=ResetPasswordSerializer)
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Пожалуйста, укажите имейл'}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(CustomUser, email=email)
        serializer = ResetPasswordSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        user.auth_token.delete()

        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
