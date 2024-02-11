from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import CompanySerializer  ,CompanyDetailSerializer,CompanyViewSerializer
from .models import Company
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination

from drf_yasg.utils import swagger_auto_schema 





class StandartPaginational(PageNumberPagination):
    page_size = 20
    page_query_param = 'page'
    def get_paginated_response(self,data):
        return Response({
            'links':{
                'next':self.get_next_link(),
                'previous':self.get_previous_link(),
            },
            'count':self.page.paginator.count,
            'results':data
        })

class CompanyCreateView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=CompanySerializer)
    def post(self, request):
        serializer = CompanySerializer(data=request.data)

        if serializer.is_valid():
            try:
                serializer.validated_data['owner'] = request.user
                company = serializer.save()

                return Response({'message':'Company is create!'})
            except Exception as e:
                return Response({'error': 'You already have company'})

        return Response({'error': 'Invalid data provided or this name is already taken'})




class Companies_view(APIView):
    def get(self,request):
        paginator = StandartPaginational()
        try:
            companies = Company.objects.all()
            pagination_companies = paginator.paginate_queryset(companies,request)
            serializer = CompanyViewSerializer(pagination_companies,many = True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'})




class CompanyDetailView(APIView):
    
    def get(self,reqeust,id):
        company = get_object_or_404(Company,id=id)
        serializer = CompanyDetailSerializer(company)
        return Response({'company':serializer.data,'message':'Successfully retrieved'})

    def delete(self,reqeust,id):
        try:
            company = get_object_or_404(Company, id = id)
            if reqeust.user == company.owner:
                company.delete()
                return Response({'message':'Company is del'})
            return Response({'error':'You don\'t have permissions for del'})
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'})