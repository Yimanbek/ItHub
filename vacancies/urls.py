from django.urls import path,include
from .views import VacanciesCreateView,VacanciesDetailDestroy,Get_object_vac,ResponseToVacancyView

urlpatterns = [
    path('create_vacancy/',VacanciesCreateView.as_view()),
    path('vacancy/<int:pk>/', VacanciesDetailDestroy.as_view()),
    path('vacancies_view/',Get_object_vac.as_view()),
    path('respond_to_vacancy/<int:vacancy_id>/', ResponseToVacancyView.as_view()),
]