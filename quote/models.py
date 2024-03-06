from django.db import models

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True,db_index=True)

    def __str__(self):
        return self.name
class Quote(models.Model):
    quote_id = models.CharField(max_length=512,db_index=True,null=True)
    author = models.CharField(max_length=120)
    content = models.TextField()
    author_slug = models.SlugField(max_length=120)
    dateadded = models.DateField()
    datemodified = models.DateField()
    tags = models.ManyToManyField(Tag)
    length = models.IntegerField(null=True)

    def __str__(self):
        return self.quote_id
