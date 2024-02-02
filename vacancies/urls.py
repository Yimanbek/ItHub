from django.urls import path
from .views import VacanciesCreateView,VacanciesDetailDestroy,get_object_vac,respond_to_vacancy

urlpatterns = [
    path('create_vacancy/',VacanciesCreateView.as_view(),name = 'create_vacancies'),
    path('vacancy/<int:pk>/', VacanciesDetailDestroy.as_view(), name='vacancy'),
    path('vacancies_view/',get_object_vac,name = 'vacancy_view'),
    path('respond_to_vacancy/<int:vacancy_id>/', respond_to_vacancy, name='respond_to_vacancy'),
]