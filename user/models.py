from datetime import datetime
from unicodedata import category
from django.db import models
from django.urls import reverse
from PIL import Image
from phonenumber_field.modelfields import PhoneNumberField
from random import randint
import uuid
from json import JSONEncoder
from uuid import UUID

from django.contrib.auth.models import User, Group
from multiselectfield import MultiSelectField

# Create your models here.
JSONEncoder_olddefault = JSONEncoder.default
def JSONEncoder_newdefault(self, o):
    if isinstance(o, UUID): return str(o)
    return JSONEncoder_olddefault(self, o)
JSONEncoder.default = JSONEncoder_newdefault

#Ticket Category Choices
FEE_CATEGORY = (
    ('70% PAYMENT', '70% PAYMENT'),
    ('COMPLETE PAYMENT', 'COMPLETE PAYMENT'),
    ('SCHOLARSHIP', 'SCHOLARSHIP'),
    ('PROJECT-BASED AGREEMENT', 'PROJECT-BASED AGREEMENT'),
)

ACTIVATION = (
    ('ACTIVATED', 'ACTIVATED'),
    ('NOT ACTIVATED', 'NOT ACTIVATED'),
)

GENDER = (
	('Male', 'Male'),
	('Female', 'Female'),
)

CATEGORY_ADMISSION = (
    ('Computer Literacy', 'Computer Literacy'),
    ('Applications Training', 'Applications Training'),
    ('Frontend Training', 'Frontend Training'),
    ('Backend Training', 'Backend Training'),
)

#User Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True)
    surname = models.CharField(max_length=20, null=True)
    othernames = models.CharField(max_length=40, null=True)
    gender = models.CharField(max_length=6, choices=GENDER, blank=True, null=True)
    phone = PhoneNumberField()
    image = models.ImageField(default='avatar.jpg', blank=False, null=False, upload_to ='profile_images', 
    )

    #Method to save Image
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
    #Check for Image Height and Width then resize it then save
        if img.height > 200 or img.width > 150:
            output_size = (150, 250)
            img.thumbnail(output_size)
            img.save(self.image.path)
 
    def __str__(self):
        return f'{self.user.username}-Profile'

class Course(models.Model):
    course_name = models.CharField(max_length=100, choices=CATEGORY_ADMISSION, null=True)
    #date = models.DateField(auto_now_add=False, auto_now=False, null=False)
    form_fee = models.CharField(max_length=200)
    course_fee = models.CharField(max_length=200)
    logo = models.ImageField(default='avatar.jpg', blank=False, null=False, upload_to ='profile_images')
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course_name}"

    #Prepare the url path for the Model
    def get_absolute_url(self):
        return reverse("event_detail", args=[str(self.id)])