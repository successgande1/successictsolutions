"""successictapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from user import views as user_views
from django.contrib.auth import views as auth_view 
from user.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('', include('dashboard.urls')),
    path('register/applicant/', user_views.register, name = 'register'),
    path('profile/', user_views.profile, name = 'user-profile'),
    path('profile/update/', user_views.profile_update, name = 'user-profile-update'),
    path('education/', user_views.add_education, name = 'user-education'),
    path('education/detail/', user_views.view_education, name = 'view-education'),
    path('add/contact/', user_views.add_contact, name = 'applicant-contact'), 
    path('referee/applicant/contacts/', user_views.view_contact_details, name = 'view-contacts'), 
    path('applicant/add/training/session/', user_views.training_sessions, name = 'applicant-session'), 
     
    path('add/course/', user_views.CourseCreateView.as_view(), name = 'create-course'),
    path('list/course/', user_views.CourseListView.as_view(), name='list-course'),
    path('delete/course/<int:course_id>', user_views.delete_course, name ='delete-course'),
    path('ticket/add/', user_views.TicketCreateView.as_view(), name = 'create-ticket'),
    # path('ticket/list/', user_views.TicketListView.as_view(), name='ticket-list'),
    path('list/tickets/', user_views.Ticket_list, name = 'list-ticket'),
    path("generate-pins/<int:ticket_id>", user_views.generate_pins_for_ticket, name="generate-pin"),
    path('activate/', user_views.pin_activation, name = 'pin-activation'), 
    path('guest/register/', user_views.register_guest, name = 'register-guest'),
    path('applicant/submit/', user_views.SubmitApp, name = 'app-submit'),
    path('applicant/codeof/conduct/', user_views.codeof_conduct, name = 'codeof_conduct'),
    path('applicant/slip/', user_views.AppSlip, name = 'app-slip'),
    path('pin/list/', user_views.PinListView.as_view(), name='pin-list'),
    path('list/pin/', user_views.Pin_Search_List, name = 'list-pin'),
    path('generated/pdf/pins/', user_views.GeneratePdf.as_view(), name = 'pdf-pins'),
    path('user/login/', auth_view.LoginView.as_view(template_name='user/login.html'), name = 'user-login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='user/logout.html'), name = 'user-logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
