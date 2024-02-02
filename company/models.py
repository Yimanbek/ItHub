from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
class Company(models.Model):
    owner = models.OneToOneField(get_user_model(),related_name = 'company',on_delete = models.CASCADE)
    name = models.CharField(unique = True,max_length = 100)
    image = models.ImageField(upload_to='company_image/')
    description = models.TextField()
    created_at = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.name