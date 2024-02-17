from django.db import models
from django.contrib import admin


# Create your models here.
class Book(models.Model):
    id = models.IntegerField(primary_key=True)
    # Assuming max book name size is 320 chars, can be changed according to requirement
    name = models.CharField(max_length=320, null=False)
    number_of_copies = models.IntegerField(null=False)

admin.site.register(Book)
