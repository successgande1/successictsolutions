from django.shortcuts import render, redirect
from django.contrib import messages
from . models import *
from . forms import *
from django.core.mail import *

# Create your views here.
def index(request):
    context = {
        
    }
    return render(request, 'pages/index.html', context)

#About Us Template Function View
def about(request):
    context = {

    }
    return render(request, 'pages/about.html', context)
#SuccessGande Custom Software Page
def software(request):
    page_title = "Custom Software"
    context = {
        'page_title':page_title,
    }
    return render(request, 'pages/custom-software.html', context)

#Contact Us View PAGE
def contact_us(request):
    
    #Page Name
    page_title = "Contact Us"
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_name = form.cleaned_data['name']
            cotact_email = form.cleaned_data['email']
            contact_phone = form.cleaned_data['phone']
            contact_subject = form.cleaned_data['subject']
            msg = form.cleaned_data['message']
            admin_msg = "Someone has contacted SUCCESSGANDE ICT Solutions with the following message; "
            
            
            
            contact = Contact.objects.create(name = contact_name, email=cotact_email, phone=contact_phone, subject=contact_subject, message=msg)
            contact.save()
            send_mail(
                'SUCCESSGANDE ICT Solutions',
                (admin_msg+msg),
                'noreply@successsolutions.com.ng',
                ['nabem.jude@gmail.com','successgande@hotmail.com'],
                
            )
            messages.success(request, f'{contact_name}, Your Message was Sent Successfully. We look forward to replying you ASAP.')
            return redirect('contact-success')

            
            
            
    else:
        form = ContactForm()
    context = {
        'form':form,
        'page_title':page_title,
    }
    return render(request, 'pages/contact-us.html', context)

def contact_success(request):
    page_title = "Success Message"
    context = {
        'page_title':page_title,
    }
    return render(request, 'pages/contact-success.html', context)
#Website Development view
def develop_website(request):
    page_title = 'Develop Website'
    context = {
        'page_title':page_title,
    }
    return render(request, 'pages/web-dev.html', context)

#Admission Process view
def admission_process(request):
    page_title = 'Admission Process'
    context = {
        'page_title':page_title,
    }
    return render(request, 'pages/admission_process.html', context)

#Training Programes view
def trainings(request): 
    page_title = 'Training'
    context = {
        'page_title':page_title,
    }
    return render(request, 'pages/training_programs.html', context)



#Pre-Application view
def pre_application(request):
    page_title = 'Pre Application' 
    context = {
        'page_title':page_title,
    }
    return render(request, 'pages/pre_application.html', context)

#computer Applications training view
def applications_training(request):
    page_title = 'Applications Training' 
    context = {
        'page_title':page_title,
    }
    return render(request, 'pages/applications_training.html', context)

#Web Programming training view
def web_programming(request):
    page_title = 'Web Programming Training' 
    context = {
        'page_title':page_title,
    }
    return render(request, 'pages/web_programming.html', context)


