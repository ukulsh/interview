from django.db import models
from django.contrib import admin

# Create your models here.
class Member(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=320, null=False)

admin.site.register(Member)
