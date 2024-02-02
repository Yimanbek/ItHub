from django.db import models
from django.contrib.auth import get_user_model
from company.models import Company
from django.utils import timezone
class Vacancies(models.Model):
    owner = models.ForeignKey(Company,related_name = 'vacancies',on_delete = models.CASCADE)
    title = models.CharField(max_length = 255)
    description = models.TextField()
    requirement = models.TextField()
    schedule = models.TextField()
    salary = models.CharField(max_length = 100)
    created_at = models.DateTimeField(default = timezone.now)


    def __str__(self):
        return self.title