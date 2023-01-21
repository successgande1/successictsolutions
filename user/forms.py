# from os import getgroups
from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from . models import *

#Create User Form
class CreateUserForm(UserCreationForm): 
    email = forms.EmailField
    #group = forms.ModelChoiceField(queryset=Group.objects.all(),
                                   #required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']