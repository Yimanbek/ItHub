from django.urls import path
from .views import CompanyCreateView,companies_view
urlpatterns = [
    path('create/',CompanyCreateView.as_view(),name = 'create_company'),
    path('companies/',companies_view,name='companies')
]