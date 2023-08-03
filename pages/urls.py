from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index, name = 'pages-home'),
    path('about/', views.about, name = 'pages-about'),
    path('affordable-web-developers-benue-state/', views.software, name= 'custom-software'),
    path('contact-us/', views.contact_us, name ="contact-us"),
    path('internet/', views.internet_of_things, name ="internet-of-things"),
    path('contact-success/', views.contact_success, name ="contact-success"),
    path('affordable-and-conducive-accommodation-in-benue-state/', views.develop_website, name ="develop-website"),
    path('training-programs/', views.trainings, name ="training-programs"),
    path('admission-process/', views.admission_process, name ="admission-process"), 
    path('pre-application/', views.pre_application, name ="Pre-Application"),
    path('applications-training/', views.applications_training, name ="applications-training"),
    path('web-programming/', views.web_programming, name ="web-programming"),
    
]