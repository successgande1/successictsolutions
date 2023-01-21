from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import F, Q
# from stockmgt.models import *
from user.forms import *
from django.shortcuts import get_object_or_404


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