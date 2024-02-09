from django.db import models
from django.contrib.auth import get_user_model

class Courses(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='course_files/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(get_user_model(),related_name = 'courses',on_delete = models.CASCADE)

    def __str__(self):
        return self.title
