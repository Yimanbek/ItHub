from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import CompanySerializer  
from django.shortcuts import render,redirect
from rest_framework.authentication import SessionAuthentication
from .models import Company

class CompanyCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get(self, request):
        return render(request, 'create_company.html')

    def post(self, request):
        serializer = CompanySerializer(data=request.data)

        if serializer.is_valid():
            try:
                serializer.validated_data['owner'] = request.user
                company = serializer.save()

                return redirect('companies')
            except Exception as e:
                return render(request,'create_company.html',{'error': 'You already have company'})

        return render(request,'create_company.html',{'error': 'Invalid data provided or this name is already taken'})

def companies_view(request):
    companies = Company.objects.all()
    return render(request,'companies.html',{'companies':companies})
