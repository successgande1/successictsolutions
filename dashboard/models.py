from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.

# #Computer Training Categories
# CATEGORY_ADMISSION = (
#     ('Computer Literacy', 'Computer Literacy'),
#     ('Computer Literacy Scholarship', 'Computer Literacy Scholarship'),
#     ('Applications Training', 'Applications Training'),
#     ('Applications Training Scholarship', 'Applications Training Scholarship'),
#     ('Frontend Training', 'Frontend Training'),
#     ('Frontend Training Scholarship', 'Frontend Training Scholarship'),
#     ('Backend Training', 'Backend Training'),
#     ('Backend Training Scholarship', 'Backend Training Scholarship'),
# ) 

#Pre-Admission Model
# class Expenditure(models.Model):  
#     course = models.CharField(max_length=100, choices=CATEGORY_ADMISSION, null=True)
#     applicant = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     amount = models.PositiveIntegerField(null=False)
#     date = models.DateField(auto_now_add=False, auto_now=False, null=False)
#     addedDate = models.DateTimeField(auto_now_add=True)
    
    

    # class Meta:
    #     verbose_name_plural = 'Expenses'

    # def __str__(self):
    #     return self.description
