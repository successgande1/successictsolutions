from django.db import models
from datetime import datetime

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=30, null=True)
    email = models.CharField(max_length=30, null=True)
    phone = models.CharField(max_length=30, null=True)
    subject = models.CharField(max_length=25, blank=True, null=True)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.name}-Message'
