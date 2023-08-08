from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.list import ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.models import User
from .process import html_to_pdf 
from django.template.loader import render_to_string
from django.views.generic.list import ListView, View
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core import paginator
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from datetime import *
from . models import *
from . forms import *
from django.db.models import F, Q
# from stockmgt.models import *
from . forms import *
from django.shortcuts import get_object_or_404
from dashboard.helpers import (
    get_profile,
    profile_complete,
    get_education,
    education_complete,
    get_contact_details,
    contact_complete,
    get_training_session,
    session_complete,
    get_question_response,
    questionnaire_complete
)


from django.contrib import messages

#Computer Literacy Admission Form Method
def register(request):

    page_title = "Register"
    if request.method == 'POST':
        form = CreateUserForm(request.POST) 
        if form.is_valid():
            form.save()
            messages.success(request, 'Registered Successfully.')
            return redirect('user-login')
    else:
        form = CreateUserForm()
    context = {
        'form':form,
        'page_title':page_title,
    }
    return render(request, 'user/register.html', context)


class CourseCreateView(LoginRequiredMixin, CreateView):
    #permission_required: 'Ticket.add_ticket'
    model = Course
    form_class =CourseCreationForm
    template_name = 'user/add_course.html'
    success_url = reverse_lazy('list-course')
    success_message = 'Course Added Successfully'

#Event List View
class CourseListView(ListView):
	template_name = 'user/course_list.html'
	queryset = Course.objects.order_by('-added_date')
	context_object_name = 'courses'

#Create Ticket View
class TicketCreateView(LoginRequiredMixin, CreateView):
    #permission_required: 'Ticket.add_ticket'
    model = Ticket
    form_class = TicketCreationForm
    template_name = 'user/add_ticket.html'
    success_url = reverse_lazy('list-ticket')
    
    # def get_success_url(self):
    #     return reverse_lazy('ticket-detail',kwargs={'pk': self.get_object().id})

#Tick List View
@login_required(login_url='user-login')
def Ticket_list(request):
    #Get Current Date
    current_date = datetime.now().date()
    #Filter Tickets whose Event is NOT YET PAST
    tickets = Ticket.objects.all()
    context = {
        'tickets':tickets,
        'current_date':current_date,
    }
    return render(request, 'user/ticket_list.html', context)

class TicketDetail(LoginRequiredMixin, DetailView):
    template_name = 'user/ticket_detail.html'
    model = Ticket

    def get_success_url(self):
        return reverse_lazy('generate-pin', kwargs = {'pk' : self.get_object().id})

#Function to Generate Pin for Tickets
@login_required(login_url='user-login')
def generate_pins_for_ticket(request, ticket_id):
    if request.user.is_superuser:
        ticket = Ticket.objects.get(id=ticket_id)
        for _ in range(20):
            Pin.objects.create(ticket=ticket)
        messages.success(request, 'You have Generated 18 PINs Ticket.')
        return redirect('pdf-pins')
    else:
        messages.success(request, 'You are not Authorize to Generate PINs for Tickets.')
        return redirect('dashboard-index')

#PIN List View
@login_required(login_url='user-login')
def Pin_Search_List(request):
    context = {}
    #Search PIN Form
    searchForm = SearchCourseTicketForm(request.GET or None)
    
    
    if searchForm.is_valid():
        #Value of search form
        value = searchForm.cleaned_data['value']
        #Filter Event Ticket PINs by Name reference
        #list_pins = Pin.objects.filter(guest___event__event_name__icontains=value)

        user_pin = Pin.objects.filter(value=value)[:1]
        
      
    else:
        user_pin = Pin.objects.order_by('-added')[:2]

    page_title = "Search and Print PINs"
    context.update ({
        'page_title':page_title,
        'list_pins':user_pin,
        'searchForm':searchForm,
        'page_title':"PIN Status",
        

    })
    return render(request, 'user/pin_list.html', context)
    
    #Set Pagination to 10/page
    # paginator = Paginator(user_pin, 10)
    # page = request.GET.get('page')
    # pin_status = paginator.get_page(page)
    


class GeneratePdf(View):
     def get(self, request, *args, **kwargs):
        data = Pin.objects.all().order_by('-added')[:20]
        open('templates/temp.html', "w").write(render_to_string('user/generated_pdf_pins.html', {'data': data}))

        # Converting the HTML template into a PDF file
        pdf = html_to_pdf('temp.html')
         
         # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')

class PinListView(ListView):
	template_name = 'user/pin_list.html'
	queryset = Pin.objects.filter(status="Not Activated")
	context_object_name = 'pins'


# #Pin Activation View
def pin_activation(request):

    if request.method == "POST":
        
        #Create new form with name form
        form = PinActivationForm(request.POST)
        #Get User Pin Value from Form
        pin_value = form['pin'].value()

        #Check if the the form has valid data in it
        if form.is_valid():
            try:
                #Get user Pin with the one in the Database
                check_pin_status = Pin.objects.get(value=pin_value)
                
            except Pin.DoesNotExist:
                messages.error(request, f'Sorry, Something Went Wrong!')
                return redirect('pin-activation')
            else:

                #Check PIN status
                if check_pin_status:
                    #Get Course Ticket Date of the PIN
                    # course_date = check_pin_status.ticket.course.date
                    # #Get Current Date
                    # current_date = datetime.now().date()
                    
                    # #Check if Event Date is Passed the Current Date
                    # if course_date < current_date:
                    #     messages.error(request, 'Course Application For Admission is Closed')
                    #     return redirect('pin-activation')
                    #Check if Event Ticket is Already Validated
                    if Pin.objects.filter(value=form['pin'].value(), status="Validated"):
                        messages.error(request, 'Already Validated, Create User Account.')
                        return redirect('register-guest')
                    #Check if PIN is ready Activated
                    elif  Pin.objects.filter(value=form['pin'].value(), status="Activated"):
                        messages.error(request, "Pin Already Activated, Login.")
                        return redirect('user-login')  

                    else:
                        #Update the User Pin with a new status of Activated
                        Pin.objects.filter(value=form['pin'].value()).update(status='Validated')
                        #Set PIN session
                        request.session['pin'] = pin_value
                        #Message the User
                        messages.success(request, 'Pin Validated Successfully')
                        #Redirect the user to register for seat
                        return redirect('register-guest')               
                #Check filter the DB where the PIN status is Validated
                               
        else:
            messages.error(request, 'Something Went Wrong. Try again')
    else:
        form = PinActivationForm()
    context = {
        'form':form,
    }
    return render(request, 'user/pin_activation.html', context)

#Register New Applicant User Method
def register_guest(request):
    #Get Value of Pin from the session
    pin = request.session.get('pin')
    
    #Try the value of PIN gotten from session with the one in the Database
    try:
        pin_detail = Pin.objects.get(value = pin)
        #Extract the Course Ticket from the PIN Session above
        pin_instance = pin_detail.ticket.course
    except Pin.DoesNotExist:
        messages.error(request, 'Sorry, Something Went Wrong. Try Again, Pls.')
        return redirect('pin-activation')
    else:
        #Guest User Registration Form
        form = GuestUserForm() 
        
        page_title = "Create Account"
        if request.method == 'POST':
            form = GuestUserForm(request.POST) 
            
            #Check if Form contains valid data
            
            if form.is_valid():
                
                #Save the Applicant User Form to get an instance of the user
                new_user = form.save()
                #Create A New Applicant with his PIN and Course Ticket
                Applicant.objects.create(app_name=new_user, course_ticket=pin_instance) 
                #Filter and update PIN
                Pin.objects.filter(value=pin).update(status='Activated')
                #Delete the PIN Session from the requet
                del request.session['pin']
                #Send User Message
                messages.success(request, 'Account Created, Login to Fill Admission Form.')
                return redirect('user-login')
        else:
            form = GuestUserForm()
            
            
        context = {
            'form':form,
            'page_title':page_title,
           
        }
        return render(request, 'user/register.html', context)


class UserListView(ListView):
    template_name = 'user/staff_list.html'
    queryset = User.objects.all()
    context_object_name = 'users'

#Delete Course View
@login_required(login_url='user-login')
def delete_course(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return redirect('course-list')

    else:
        course_name = course.course_name

        if request.method == "POST":
            course.delete()
            messages.error(request, f'{course_name} Course Deleted Successfully.')
            return redirect('list-course')
        
        page_title = "Delete Course"
        context = {
            'page_title':page_title,
            'course_name':course_name,

        }
        return render(request, 'user/delete_confirm.html', context)
    
#View Profile Method
@login_required(login_url='user-login')
def profile(request):
    if 'user' not in request.session:
        return redirect('user-login')
    else:
        context = {   
        'page_title':'Profile',
        }
        return render(request, 'user/profile.html', context)
   
#Update Profile Method
@login_required(login_url='user-login')
def profile_update(request):
    if request.method == 'POST':
        #create user form variable
        user_form = UserUpdateForm(request.POST, instance=request.user)
        #create update form variable
        

        profile_form = ProfileUpdateForm(request.POST, request.FILES, 
        instance=request.user.profile)
    #Check if both forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            
            #Check if it exist
            if not profile_form.cleaned_data.get('image'):
                messages.error(request, 'You Need to upload an Image')
                return redirect('user-profile-update')
            else:
                user_form.save()
                profile_form.save()
                messages.success(request, 'Profile Updated Successfully.')
                return redirect('user-education')
            #profile_form.cleaned_data['profilestatus'] ='Updated'
            
            # image = profile_form.cleaned_data['image']

            # if not image:
            #     messages.error(request, 'Passport is Needed.')
            #     return redirect('user-profile-update')

            # else:
                
        else:
            messages.error(request, 'Check Your Passport Image.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'user/profile_update.html', context)

@login_required(login_url='user-login')
def add_education(request):
    user = request.user
    if not user.is_superuser: #Check if is not Admin User then add Education Record
        try:
            check_education = Education.objects.get(applicant=request.user)
       
        except Education.DoesNotExist:
         #Check if the form method is POST
            if request.method == 'POST':
                #Grab the Add Education Form with information and files
                form = AddEducationForm(request.POST, request.FILES)
                #Check if the form is valid
                if form.is_valid():
                    #Attach the logged in applicant to the Education Form (User instance)
                    form.instance.applicant = request.user
                    #Save the form
                    form.save()
                    #Send Success Message
                    messages.success(request, 'Education Added, Review Details To Continue.')
                    return redirect('applicant-contact')
            else:
                form = AddEducationForm()
            context = {
            'form':form,
            }
            return render(request, 'user/add_education.html', context) 
        else:
            if check_education.qualification != None:
                return redirect('view-education')
            else:
                return redirect('app-submit')
    else:
        return redirect('user-profile')
        
#Method for viewing Education Detail
class EducationDetail(LoginRequiredMixin, DetailView):
    """Applicant View Education Details"""
    template_name = 'user/education_detail.html'
    model = Education
    page_title = 'View Education'

    def get_success_url(self):
        return reverse_lazy('applicant-contact', kwargs = {'pk' : self.get_object().id})
    
class UpdateEducationDetails(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'user/add_education.html'
    form_class = AddEducationForm
    model = Education 
    page_title = 'Edit Education'

    
    #Function to get Object Key for url
    def get_success_url(self):
        return reverse_lazy('view-education', kwargs = {'pk':self.get_object().id})
    
    def test_func(self):
        return self.get_object().applicant_id == self.request.user.pk 
    


@login_required(login_url='user-login')
def add_contact(request):
    try:
       check_contact = Contactdetails.objects.get(applicant=request.user)
       
    except Contactdetails.DoesNotExist:
         #Check if the form method is POST
        if request.method == 'POST':
            #Grab the Add contact Form with information and files
            form = AddContactDetailForm(request.POST, request.FILES)
            #Check if the form is valid
            if form.is_valid():
                #Attach the logged in applicant to the contact Form (User instance)
                form.instance.applicant = request.user
                #Save the form
                form.save()
                #Send Success Message
                messages.success(request, 'Contact Details Added Successfully')
                return redirect('applicant-session')
        else:
            form = AddContactDetailForm()
        context = {
            'form':form,
            'page_title': 'Add Contact',
        }
        return render(request, 'user/add_contact.html', context) 
    else:
        if contact_complete(check_contact) :
            return redirect('dashboard-index')
        else:
            return redirect('app-submit')

    
#Applicant Edit Contact Details
class UpdateContactDetails(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'user/add_contact.html'
    form_class = AddContactDetailForm
    model = Contactdetails 
    page_title = 'Edit Contact'

    
    #Function to get Object Key for url
    def get_success_url(self):
        return reverse_lazy('contact-details', kwargs = {'pk':self.get_object().id})

    def test_func(self):
        return self.get_object().applicant_id == self.request.user.pk 
    
class ContactDetail(LoginRequiredMixin, DetailView):
    """Applicant View Contact Details"""
    template_name = 'user/applicant_contacts.html'
    model = Contactdetails
    page_title = 'View Contacts'

    #Get Context Data on the HTML
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

    def get_success_url(self):
        return reverse_lazy('applicant-session', kwargs = {'pk' : self.get_object().id})
    

    
   
@login_required(login_url='user-login')
def training_sessions(request):
    #check if user is in the session
    logged_user = request.user
    questionnaire = get_question_response(logged_user)
    if 'user' not in request.session:
        messages.error(request, 'Something Went Wrong')
        return redirect('user-login')
    else:
        try:
            user_training_session = Tsessions.objects.get(applicant=request.user)
        except Tsessions.DoesNotExist:
                if request.method == 'POST':
                    #Grab the Add Training Session Form with information and files
                    form = AddTrainingSessionForm(request.POST, request.FILES)
                    #Check if the form is valid
                    if form.is_valid():
                        
                        #Attach the logged in applicant to the Training Session Form (User instance)
                        form.instance.applicant = request.user
                        training_session_name = form.cleaned_data.get('training_session')
                        training_days_name = form.cleaned_data.get('training_days')
                        #Save the form
                        form.save()
                        #Send Success Message
                        messages.success(request, f'{training_session_name}, {training_days_name} Choosen for  {request.user.applicant.course_ticket}  Course')
                        return redirect('codeof_conduct')
                else:
                    form = AddTrainingSessionForm()
                context = {
                    'form':form,
                    'page_title' : 'Add Session'
                }
                return render(request, 'user/training_sessions.html', context) 
        else:
            if session_complete(user_training_session) and questionnaire_complete(questionnaire) :
                return redirect('app-submit')
            else:
                return redirect('user-login')
                

    
class UpdateTrainingSessionDetails(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'user/training_sessions.html'
    form_class = AddTrainingSessionForm
    model = Tsessions 
    page_title = 'Edit Training Session'

    #Get Context Data on the HTML
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

    
    #Function to get Object Key for url
    def get_success_url(self):
        return reverse_lazy('view-session', kwargs = {'pk':self.get_object().id})
    
    def test_func(self):
        return self.get_object().applicant_id == self.request.user.pk 

class TrainingSessionDetail(LoginRequiredMixin, DetailView):
    """Applicant View Session Details"""
    template_name = 'user/applicant_session.html'
    model = Tsessions
    page_title = 'View Training Session'

    #Get Context Data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

    def get_success_url(self):
        return reverse_lazy('app_view_questions', kwargs = {'pk' : self.get_object().id})
            
#Applicant Answer Questionnaire View
@login_required(login_url='user-login')
def questionnaire(request):
    logged_user = request.user
    questionnaire = get_question_response(logged_user)
    if 'user' not in request.session:
        messages.error(request, 'Something Went Wrong')
        return redirect('user-login')
    elif questionnaire_complete(questionnaire): #Check if Questionnaire is submitted
        return redirect('app-submit') 
    else:
        app_course = Applicant.objects.get(app_name=request.user)
        Applicant_course = app_course.course_ticket.course_name

        if request.method == 'POST':
            form = AddQuestionnaireForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.applicant = request.user
                form.save()
                        #Send Success Message
                messages.success(request, f'Questionnaire for {Applicant_course} Course Submitted Successfully'  )
                return redirect('app-submit')
            
        else:
            form = AddQuestionnaireForm()
        context = {   
            'Applicant_course':Applicant_course,
        'page_title':'Questionnaire',
        'form':form,
        }
        return render(request, 'user/questionnaire.html', context)
    
class UpdateQuestionnaireDetails(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'user/questionnaire.html'
    form_class = AddQuestionnaireForm
    model = Questionnaire 
    page_title = 'Edit Response'

    #Get Context Data on the HTML
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

    
    #Function to get Object Key for url
    def get_success_url(self):
        return reverse_lazy('view-response', kwargs = {'pk':self.get_object().id})
    
    def test_func(self):
        return self.get_object().applicant_id == self.request.user.pk 

class QuestionnaireDetail(LoginRequiredMixin, DetailView):
    """Applicant View Questionnaire Details"""
    template_name = 'user/app_questionnaire.html'
    model = Tsessions
    page_title = 'View Responses'

    #Get Context Data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

    def get_success_url(self):
        return reverse_lazy('app-submit', kwargs = {'pk' : self.get_object().id})
    
    
        
@login_required(login_url='user-login')
def SubmitApp(request):
    try:
        #Grab the logged in applicant in the submited app table
        check_submited = Submitted.objects.get(applicant=request.user)
    #If it Does NOT Exist then submit it
    except Submitted.DoesNotExist:
        if request.method == 'POST':
            form = ConfirmForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.applicant = request.user
                form.save()
                messages.success(request, 'Application Form for Admission Submitted Successfully.')
                return redirect('app-slip')
        else:
            form = ConfirmForm()
    
        context = {
            'form':form,
            
        }
        return render(request, 'user/confirmation.html', context)

    else:
        if check_submited.application != "":
            return redirect('app-slip')      


#Function for Application Confirmation
@login_required(login_url='user-login')
def AppSlip(request):
    #Get Applicant Education Level
    get_applicant = Applicant.objects.get(app_name = request.user)
    
    candidate_choice_course = get_applicant.course_ticket

    context = {
        'candidate_choice_course':candidate_choice_course, 
    }
    return render(request, 'user/slip.html', context)  


    
   
        

    