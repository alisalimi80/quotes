from django.db import models

# Create your models here.

class Qoute(models.Model):
    author = models.CharField(max_length=120)
    content = models.TextField()
    author_slug = models.SlugField(max_length=120)
    dateadded = models.DateField()
    datemodified = models.DateField(auto_now=True)
