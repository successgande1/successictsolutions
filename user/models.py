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
    ('Computer Litracy Application Form', 'Computer Litracy Application Form'),
    ('Computer Applications Training Form', 'Computer Applications Training Form'),
    ('Front-End Web Development Form', 'Front-End Web Development Form'),
    ('Backend Training Fee', 'Backend Training Fee'),
    ('Computer. Lit. Training Fee', 'Computer. Lit. Training Fee'),
    ('APP. Training Fee', 'APP. Training Fee'),
    ('Frontend Training Fee', 'Frontend Training Fee'),
    ('Frontend Scholarship Training', 'Frontend Scholarship Training'),
    ('Backend. Training Fee', 'Backend. Training Fee'),
    ('Project-Based Training Agreement Form', 'Project-Based Training Agreement Form'),
)

ACTIVATION = (
    ('ACTIVATED', 'ACTIVATED'),
    ('NOT ACTIVATED', 'NOT ACTIVATED'),
)

GENDER = (
	('Male', 'Male'),
	('Female', 'Female'),
)

MARITAL_STATUS = (
	('Single', 'Single'),
	('Married', 'Married'),
	('Diovioced', 'Diovioced'),
)

CONTACT_RELATIONSHIP = (
	('Father', 'Father'),
	('Mother', 'Mother'),
	('Uncle', 'Uncle'),
    ('Auntie', 'Auntie'),
    ('Brother', 'Brother'),
    ('Sister', 'Sister'),
    ('Others', 'Others'),    
)


CATEGORY_ADMISSION = (
    ('Computer Literacy', 'Computer Literacy'),
    ('Applications Training', 'Applications Training'),
    ('Frontend Training', 'Frontend Training'),
    ('Backend Training', 'Backend Training'),
)

INSTITUTE = (
    ('Secondary School', 'Secondary School'),
    ('OND', 'OND'),
    ('ND', 'ND'),
    ('HND', 'HND'),
    ('NCE', 'NCE'),
    ('Degree', 'Degree'),
)

COURSE_DURATION = (
    ('THREE MONTHS', 'THREE MONTHS'),
    ('SIX MONTHS', 'SIX MONTHS'),
    ('NINE MONTHS', 'NINE MONTHS'),
)

TRAINING_SESSIONS = (
    ('MORNING SESSION', 'MORNING SESSION'),
    ('EVENING SESSION', 'EVENING SESSION'),
    ('ONLINE NIGHT SESSION', 'ONLINE NIGHT SESSION'),
)

TRAINING_DAYS = (
    ('MONDAY - FRIDAY', 'MONDAY - FRIDAY'),
    ('WEEKENDS', 'WEEKENDS'),
)

YES_NO = (
    ('YES', 'YES'),
    ('NO', 'NO'),
)


#User Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True)
    surname = models.CharField(max_length=20, null=True)
    othernames = models.CharField(max_length=40, null=True)
    gender = models.CharField(max_length=6, choices=GENDER, blank=True, null=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS, blank=True, null=True)
    age = models.CharField(max_length=3, null=True)
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
    
class Education(models.Model):
    applicant = models.OneToOneField(User, on_delete=models.CASCADE, null = True)
    qualification = models.CharField(max_length=60, choices=INSTITUTE, default=None, null=True)
    instition = models.CharField(max_length=200, null=True)
    graduation = models.CharField(max_length=100, null=True) 
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.applicant}-Education'


class Contactdetails(models.Model):
    applicant = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    state_origin = models.CharField(max_length=40, null=True)
    lga_origin = models.CharField(max_length=30, null=True)
    phone = PhoneNumberField()
    home_town = models.CharField(max_length=30, null = True)
    village = models.CharField(max_length=30, null=True)
    permanent_address = models.CharField(max_length=200, null=True)
    contact_person = models.CharField(max_length=40, null=True)
    contact_phone = PhoneNumberField()
    contact_occupation = models.CharField(max_length=200, null = True)
    contact_relationship = models.CharField(max_length=30, choices=CONTACT_RELATIONSHIP, null=True)

    def __str__(self):
        return f'{self.applicant}-Contact'
    
class Tsessions(models.Model):
    applicant = models.OneToOneField(User, on_delete=models.CASCADE, null = True)
    training_session = models.CharField(max_length=200, choices=TRAINING_SESSIONS, default=None, null=True)
    training_days = models.CharField(max_length=200, choices=TRAINING_DAYS, default=None, null=True)
    
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.applicant}-Training Sessions'

# #Student Table
# class Student(models.Model):
#     sid = models.CharField(max_length=10, primary_key=True)
#     suser = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
#     mstatus = models.CharField(max_length=20, choices=MARITAL_STATUS, null=True)
#     sage = models.IntegerField(null=True)
    
    
#     def __str__(self):
#         return f'{self.suser}-Profile'


class Course(models.Model):
    course_name = models.CharField(max_length=100, choices=CATEGORY_ADMISSION, null=True)
    logo = models.ImageField(default='avatar.jpg', blank=False, null=False, upload_to ='profile_images')
    duration = models.CharField(max_length=100, choices=COURSE_DURATION, null=True)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course_name}"

    #Prepare the url path for the Model
    def get_absolute_url(self):
        return reverse("event_detail", args=[str(self.id)])
    

#Ticket Model
class Ticket(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    category = models.CharField(max_length=255, choices=FEE_CATEGORY, default=None, blank=True, null=True)
    added_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.course} "

    #Prepare the url path for the Model
    def get_absolute_url(self):
        return reverse("ticket-detail", args=[str(self.id)])

def generate_pin():
    return ''.join(str(randint(0, 9)) for _ in range(6))

class Pin(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    value = models.CharField(max_length=6, default=generate_pin, blank=True)
    added = models.DateTimeField(auto_now_add=True,  blank=False)
    reference = models.UUIDField(primary_key = True, editable = False, default=uuid.uuid4)
    status = models.CharField(max_length=30, default='Not Activated')
    
    #Save Reference Number
    def save(self, *args, **kwargs):
         self.reference == str(uuid.uuid4())
         super().save(*args, **kwargs) 

    def __unicode__(self):
        return self.ticket

    class Meta:
        unique_together = ["ticket", "value"]

    def __str__(self):
        return f"{self.ticket}"

    def get_absolute_url(self):
        return reverse("pin-detail", args=[str(self.id)])

class Applicant(models.Model):
    app_name = models.OneToOneField(User, on_delete=models.CASCADE, blank=True) 
    course_ticket = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True) 
    added_date = models.DateField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.guest_name}" 

class Studentcourse(models.Model):
    courseid = models.CharField(max_length=10, primary_key=True)
    student = models.ForeignKey(Applicant, on_delete=models.CASCADE, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True)
    added_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.courseid}" 
    
class questionnaire(models.Model):
    applicant = models.OneToOneField(User, on_delete=models.CASCADE, blank=True) 
    computer_knowledge = models.CharField(max_length=100, choices=YES_NO, null=True)
    own_laptop = models.CharField(max_length=200, null=True)
    own_phone = models.CharField(max_length=200, null=True)
    browse_internet = models.CharField(max_length=200, null=True)
    know_programming = models.CharField(max_length=200, null=True)
    learn_night = models.CharField(max_length=200, null=True)
    added_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant}" 
    

class Submitted(models.Model):
    applicant = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    application = models.UUIDField(primary_key = True, editable = False, default=uuid.uuid4)
    confirm = models.BooleanField()
    approved = models.CharField(max_length=20, null=True, default='Not Approved')
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
         self.application == str(uuid.uuid4())
         super().save(*args, **kwargs)

    def __unicode__(self):
        return self.applicant 

    def __str__(self):
        return f'Application Number: {self.application}-{self.applicant}'
    
class Employee(models.Model):
    STAFF_CATEGORY = [
        ('Instructor', 'Instructor'),
        ('Computer Operator', 'Computer Operator'),
        ('Cashier', 'Cashier'),
    ]
    staff_user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    staff_id = models.UUIDField(primary_key = True, editable = False, default=uuid.uuid4)
    staff_role = models.CharField(max_length=20, choices=STAFF_CATEGORY, default=None, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Application Number: {self.staff_user}-{self.staff_role}'

