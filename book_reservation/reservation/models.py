from django.db import models
from django.contrib import admin

# Create your models here.
class Reserve(models.Model):
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE)
    member = models.ForeignKey('members.Member', on_delete=models.CASCADE)
    # Todo: Add index on reserved_on for faster processing
    reserved_on = models.DateTimeField(null=False, db_index=True)
    processed = models.BooleanField(default=False, db_index=True)

admin.site.register(Reserve)
