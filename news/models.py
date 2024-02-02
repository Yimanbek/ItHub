from django.db import models
from company.models import Company
from django.utils import timezone


class News(models.Model):
    owner = models.ForeignKey(Company,related_name='news', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=False)
    text = models.TextField()
    image = models.ImageField(upload_to='news_images/')
    place = models.CharField(max_length=255,blank=True)
    links = models.CharField(max_length=255,blank=True)
    created_at = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return f'{self.title}'
