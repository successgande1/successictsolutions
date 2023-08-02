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
class GuestUserForm(UserCreationForm): 
    email = forms.EmailField
   
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    
    class Meta:
        model = User
        fields = ['username', 'email']

# #Update Profile Form
class ProfileUpdateForm(forms.ModelForm):
    surname = forms.CharField(label='Surname:', widget=forms.TextInput(attrs={'placeholder': 'Inherited Family Name.'}))
    othernames = forms.CharField(label='Other Names:', widget=forms.TextInput(attrs={'placeholder': 'Personal Name(s).'}))
    
    age = forms.CharField(label='Age:', widget=forms.TextInput(attrs={'placeholder': 'Applicant\'s Age.'}))
    
   
    image = forms.ImageField(required=True)
    class Meta:
        model = Profile
        fields = ['surname', 'othernames', 'gender', 'marital_status', 'age', 'image'] 

# #Create Guest User Form
class AddStaffForm(forms.ModelForm):
    
    instition = forms.CharField(label="Institution Name :", 
                    widget=forms.TextInput(attrs={'placeholder': 'Applicant\'s Institution Full Name and Address of Institution'}))
    
    graduation = forms.CharField(label="Year of Graduation:", 
                    widget=forms.TextInput(attrs={'placeholder': 'Applicant\'s Year of Graduation'}))
    
    class Meta:
        model = Education
        fields = ['qualification','instition',  'graduation']



class AddEducationForm(forms.ModelForm):
    
    instition = forms.CharField(label="Institution Name :", 
                    widget=forms.TextInput(attrs={'placeholder': 'Applicant\'s Institution Full Name and Address of Institution'}))
    
    graduation = forms.CharField(label="Year of Graduation:", 
                    widget=forms.TextInput(attrs={'placeholder': 'Applicant\'s Year of Graduation'}))
    
    class Meta:
        model = Education
        fields = ['qualification','instition',  'graduation']


class AddContactDetailForm(forms.ModelForm):
    
    state_origin = forms.CharField(label="State of Origin :", 
                    widget=forms.TextInput(attrs={'placeholder': 'Applicant\'s State of Origin'}))
    
    lga_origin = forms.CharField(label="Local Govt. Origin:", 
                    widget=forms.TextInput(attrs={'placeholder': 'Applicant\'s Local Govt. of Origin'}))
    
    contact_person = forms.CharField(label="Referee Full Name:", 
                    widget=forms.TextInput(attrs={'placeholder': 'Applicant\'s Referee Full Name'}))
    
    contact_phone = forms.CharField(label="Referee Phone Number:", 
                    widget=forms.TextInput(attrs={'placeholder': 'Applicant\'s Referee Phone Number'}))
    
    contact_occupation = forms.CharField(label="Referee Occupation:", 
                    widget=forms.TextInput(attrs={'placeholder': 'Applicant\'s Referee Occupation'}))
    
    
    
    class Meta:
        model = Contactdetails
        fields = ['state_origin','lga_origin',  'phone', 'home_town', 'village', 'permanent_address', 'contact_person', 'contact_phone', 'contact_occupation', 'contact_relationship']

class EditContactDetailForm(forms.ModelForm):
    
    state_origin = forms.CharField(label="State of Origin :", 
                    widget=forms.TextInput(attrs={'placeholder': 'Applicant\'s State of Origin'}))
    
    lga_origin = forms.CharField(label="Local Govt. Origin:", 
                    widget=forms.TextInput(attrs={'placeholder': 'Applicant\'s Local Govt. of Origin'}))
    
    contact_person = forms.CharField(label="Referee Full Name:", 
                    widget=forms.TextInput(attrs={'placeholder': 'Applicant\'s Referee Full Name'}))
    
    contact_phone = forms.CharField(label="Referee Phone Number:", 
                    widget=forms.TextInput(attrs={'placeholder': 'Applicant\'s Referee Phone Number'}))
    
    contact_occupation = forms.CharField(label="Referee Occupation:", 
                    widget=forms.TextInput(attrs={'placeholder': 'Applicant\'s Referee Occupation'}))
    
    
    
    class Meta:
        model = Contactdetails
        fields = ('state_origin','lga_origin',  'phone', 'home_town', 'village', 'permanent_address', 'contact_person', 'contact_phone', 'contact_occupation', 'contact_relationship')

#Add Training Session Form
class AddTrainingSessionForm(forms.ModelForm):
    
    class Meta:
        model = Tsessions
        fields = ['training_session','training_days']

#Add Questionnaire Form for Computer Literacy
class AddQuestionnaireForm(forms.ModelForm):
    own_laptop = forms.CharField(label="Do You Own a Usable Laptop? :", 
                    widget=forms.TextInput(attrs={'placeholder': 'Answer Yes or No'}))
    
    own_phone = forms.CharField(label="Do You Have SmartPhone?:", 
                    widget=forms.TextInput(attrs={'placeholder': 'Answer Yes or No'}))
    
    browse_internet = forms.CharField(label="Can You Browse Internet?:", 
                    widget=forms.TextInput(attrs={'placeholder': 'Answer Yes or No'}))
    
    know_programming = forms.CharField(label="Any Programming Knowledge?:", 
                    widget=forms.TextInput(attrs={'placeholder': 'Answer Yes or No'}))
    
    learn_night = forms.CharField(label="Can You Learn All-Night?:", 
                    widget=forms.TextInput(attrs={'placeholder': 'Answer Yes or No'}))
    
    class Meta:
        model = Questionnaire
        fields = ['computer_knowledge', 'own_laptop', 'own_phone', 'browse_internet','know_programming','learn_night']



#Date Picket Widgets for date field for Event Form
class CourseDateField(forms.DateInput):
    input_type = 'date' 

#Add Event Form
class CourseCreationForm(forms.ModelForm):
    
    class Meta:
        widgets = {'date':CourseDateField()}
        model = Course
        fields = ['course_name','duration', 'logo']


#Add Ticket Form
class TicketCreationForm(forms.ModelForm):
    
    
    price = forms.CharField(label="Ticket Price :", 
                    widget=forms.TextInput(attrs={'placeholder': 'Amount to be Paid on Ticket'}))
    
    # refphone = PhoneNumberField(
    #     widget = PhoneNumberPrefixWidget(initial="NG")
    # )
    
    
    class Meta:
        model = Ticket
        fields = ['course','price', 'category']

#
class PinActivationForm(forms.Form):
    pin = forms.IntegerField(label='Pin', min_value=6)

    def clean_pin(self):
        form = self.cleaned_data['pin']

 #Search Event Ticket PINs
class SearchCourseTicketForm(forms.Form): 
    value = forms.CharField(label = 'PIN', max_length=30)


class ConfirmForm(forms.ModelForm):
    confirm = forms.BooleanField()
    class Meta:
        model = Submitted
        fields = ['confirm'] 