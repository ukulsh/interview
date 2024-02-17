from django.db import models
from django.contrib import admin

# Create your models here.
class Circulation(models.Model):
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE)
    member = models.ForeignKey('members.Member', on_delete=models.CASCADE)
    circulated_on = models.DateTimeField(null=False, db_index=True)
    returned_on = models.DateTimeField(null=True, db_index=True)
    fine_due = models.IntegerField(null=True)

admin.site.register(Circulation)
