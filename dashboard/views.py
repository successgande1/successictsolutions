from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import F, Q
# from stockmgt.models import *
# from stockmgt.forms import *
from django.shortcuts import get_object_or_404


from django.contrib import messages


@login_required(login_url='user-login')
def index(request):
    page_title = 'Dashboard'
    
    context = {
               
        }
    return render(request, 'dashboard/index.html', context)