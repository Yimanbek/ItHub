from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import VacanciesSerializer, VacanciesDetailSerializer,VacanciesListSerializer
from rest_framework import permissions
from .models import Vacancies
from account.permissions import IsAuthor,IsAuthorOrAdmin
from django.http import Http404, HttpResponse
from ithub.tasks import send_respond_data_task
from django.contrib.auth.decorators import login_required
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
    

class VacanciesCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=VacanciesSerializer)
    def post(self, request):
        try:
            serializer = VacanciesSerializer(data=request.data)
            if serializer.is_valid():
                try:
                    if request.user.is_authenticated:
                        serializer.validated_data['owner'] = request.user.company
                        user = serializer.save()
                        if user:
                            return Response({'message': 'Your request was saved successfully!', 'vacancy_id': user.id})
                        else:
                            return Response({'error': 'Your request didn\'t save!'})
                    else:
                        return Response({'error': 'You don\'t have the necessary permissions!'})
                except Exception as e:
                    return Response({'error': f'An error occurred: {str(e)}'})
            else:
                return Response({'error': 'Invalid data'})
        except Exception as e:
            return Response({'error': str(e)})


class VacanciesDetailDestroy(APIView):
    permission_classes = [permissions.AllowAny]

    serializer_class = VacanciesDetailSerializer

    def get_object(self, pk):
        try:
            return Vacancies.objects.get(pk=pk)
        except Vacancies.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        vacancy = self.get_object(pk)
        serializer = VacanciesDetailSerializer(vacancy)
        return Response(serializer.data)
    
    def delete(self,request,pk):
        try:
            vacancy = get_object_or_404(Vacancies,id=pk)
            if request.user == vacancy.owner.owner:
                vacancy.delete()
                return Response({'message':'Vacancy is delete!'})
            return Response({'error':'You don\'t have permissions for del'})
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'})



class Get_object_vac(APIView):
    def get(self,request):
        vacancies = Vacancies.objects.all()
        serializer = VacanciesListSerializer(instance = vacancies,many = True)
        return Response(serializer.data)


class ResponseToVacancyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,vacancy_id):
        vacancy = get_object_or_404(Vacancies, pk=vacancy_id)
        if request.method == 'POST':
            full_name = request.data.get('full_name')
            characteristics = request.data.get('characteristics')
            phone_number = request.data.get('phone_number')
            email = request.data.get('email')
            short_intro = request.data.get('short_intro')
            additional_info = request.data.get('additional_info')

            send_respond_data_task(full_name, characteristics, phone_number, email, short_intro, additional_info, vacancy.owner.owner)

            return Response({'message': 'Your response has been sent successfully!'})
        else:
            serializer = VacanciesDetailSerializer(vacancy)
            return Response({'message': 'Successfully retrieved'})
