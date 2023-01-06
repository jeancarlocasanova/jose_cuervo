from django.db import models
from django.urls import reverse

# Create your models here.
class Project(models.Model):
    tittle = models.CharField(max_length=50)
    description = models.CharField(max_length=50)

    def get_absolute_url(self):
        return reverse('project-list',kwargs={})
