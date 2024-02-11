from django.shortcuts import render
from rest_framework.views import APIView 
from account.models import CustomUser
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request,'home.html')



@login_required
def profile(request):
    user = request.user
    prof = CustomUser.objects.get(pk=user.id)
    return render(request, 'profile.html', {'user': prof})