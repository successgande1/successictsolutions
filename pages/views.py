from django.shortcuts import render

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
