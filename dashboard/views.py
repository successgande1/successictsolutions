from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import F, Q
from user.models import *
from .helpers import (
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
from django.shortcuts import get_object_or_404

from django.contrib.auth import logout
from django.contrib import messages


@login_required(login_url='user-login')
def index(request):
    logged_user = request.user

    if not logged_user.is_authenticated:
        messages.warning(request, 'Not Logged In')
        return redirect('user-login')
    
    # Set 'user' in session
    request.session['user'] = 'user'

    if 'user' in request.session:#Check for user session

        if hasattr(logged_user, 'user') and not hasattr(logged_user, 'applicant'):
            # Using the Helpers function, Check if User Profile is completed with a new image uploaded
            profile = get_profile(logged_user)
            if not profile_complete(profile):
                return redirect('user-profile-update')
            else:
                return redirect('user-profile')
            
        elif hasattr(logged_user, 'applicant'):
            profile = get_profile(logged_user)
            if not profile_complete(profile):
                return redirect('user-profile-update')
            #Using the help function get the Education Record of logged in user
            education = get_education(logged_user)
            if not education_complete(education):
                return redirect('user-education')

            contact = get_contact_details(logged_user)
            if not contact_complete(contact):
                return redirect('applicant-contact')

            trainingsession = get_training_session(logged_user)
            if not session_complete(trainingsession):
                return redirect('applicant-session')
            
            #Using the help function get the questionnaire of logged in user
            questionnaire = get_question_response(logged_user)
            if not questionnaire_complete(questionnaire):
                return redirect('questionnaire')

            return redirect('app-submit')

        else:
            messages.warning(request, 'No Profile Found')
            return redirect('user-login')
    else:
            messages.error(request, 'Not Logged In')
            return redirect('user-login')
        
    
                          
                          



    

       

        
                
                

               
        
        
    