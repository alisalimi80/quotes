from django.db import models

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

class Quote(models.Model):
    author = models.CharField(max_length=120)
    content = models.TextField()
    author_slug = models.SlugField(max_length=120)
    dateadded = models.DateField()
    datemodified = models.DateField(auto_now=True)
    tags = models.ManyToManyField(Tag)
