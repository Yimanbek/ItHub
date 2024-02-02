from django.shortcuts import render , redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import VacanciesSerializer,VacanciesDetailSerializer
from rest_framework import permissions
from .models import Vacancies
from account.permissions import IsAuthor
from django.http import Http404,HttpResponse
from ithub.tasks import send_respond_data_task

class VacanciesCreateView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return render(request, 'create_vacancies.html')  
    
    def post(self, request):
        try:
            serializer = VacanciesSerializer(data=request.data)
            if serializer.is_valid():
                try:
                    if request.user.is_authenticated:
                        serializer.validated_data['owner'] = request.user.company
                        user = serializer.save()
                        if user:
                            
                            return redirect('vacancy_view')
                        else:
                            return render(request,'create_vacancies.html',{'error': 'Your request didn\'t save!'})
                    else:
                        return render(request,'create_vacancies.html',{'error': 'You don\'t have the necessary permissions!'})
                except Exception as e:
                    return render(request,'create_vacancies.html',{'error': f'An error occurred: {str(e)}'})
            else:
                return render(request,'create_vacancies.html',{'error': 'Invalid data'})
        except Exception as e:
            return render(request, 'create_vacancies.html', {'error': str(e)})




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
        return render(request,'vacancy.html',{'vacancy':vacancy})


def get_object_vac(request):
    template_name = 'vacancies_view.html'
    vacancies = Vacancies.objects.all()
    return render(request,template_name,{'vacancies':vacancies})

from django.contrib.auth.decorators import login_required


@login_required
def respond_to_vacancy(request, vacancy_id):
    vacancy = get_object_or_404(Vacancies, pk=vacancy_id)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        characteristics = request.POST.get('characteristics')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        short_intro = request.POST.get('short_intro')
        additional_info = request.POST.get('additional_info')

        send_respond_data_task(full_name, characteristics, phone_number, email, short_intro, additional_info, vacancy.owner.owner)

        return redirect('vacancy', pk=vacancy.id)
    else:
        return render(request, 'respond_to_vacancy.html', {'vacancy': vacancy})