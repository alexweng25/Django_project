from django.core import validators
from django.db import models
from django.utils import timezone

# Create your models here.

class Post(models.Model):		
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    #photo = models.URLField(blank=True)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
      return self.title

class Photos(models.Model):
    image = models.ImageField(upload_to='photo',  blank=True, null=False)
    upload_date = models.DateField(default=timezone.now)
    def __str__(self):
        return self.image.name
