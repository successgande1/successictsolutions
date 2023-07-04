from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import F, Q
from user.models import *
# from stockmgt.forms import *
from django.shortcuts import get_object_or_404


from django.contrib import messages


@login_required(login_url='user-login')
def index(request):
    #Get the Logged in User
    loged_user = request.user
    #Assign the user to the session
    
    try:
        user_profile = Profile.objects.get(user=loged_user)
    except Profile.DoesNotExist:
        messages.error(request, 'Something Went Wrong')
        return redirect('user-login')
    else:
        #Get username for the user session
        request.session['user'] = request.user.username
        if user_profile.surname or request.user.is_superuser:
            return redirect('user-profile')
        else:
            return redirect('user-profile-update')
            
            
        