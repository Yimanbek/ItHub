from django.urls import path,include
from .views import VacanciesCreateView,VacanciesDetailDestroy,Get_object_vac,ResponseToVacancyView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', Get_object_vac)
urlpatterns = [
    path('create_vacancy/',VacanciesCreateView.as_view()),
    path('vacancy/<int:pk>/', VacanciesDetailDestroy.as_view()),
    path('vacancies_view/',include(router.urls)),
    path('respond_to_vacancy/<int:vacancy_id>/', ResponseToVacancyView.as_view()),
]