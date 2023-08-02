from django.contrib import admin
from . models import * 

# Register your models here.

#Register Admin Profile Table
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'surname', 'othernames', 'gender', 'image')
    list_per_page = 25
#Register Profile Table
admin.site.register(Profile, ProfileAdmin)

#Register Admin Course Table
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'duration', 'added_date')
    list_per_page = 25


class TicketAdmin(admin.ModelAdmin):
    list_display = ('course', 'price', 'category', 'added_date')
    list_per_page = 25

class PinAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'value', 'added', 'reference', 'status')
    list_per_page = 25

class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('app_name', 'course_ticket', 'added_date')
    list_per_page = 25

# class StudentAdmin(admin.ModelAdmin):
#     list_display = ('sid', 'suser', 'mstatus', 'sage', 'sorigin', 'slga', 'homet', 'village', 'paddress', 'cperson', 'coccupation', 'cprelationship')
#     list_per_page = 25

#Register Course Table
admin.site.register(Course, CourseAdmin)

admin.site.register(Ticket, TicketAdmin)

admin.site.register(Pin, PinAdmin)

admin.site.register(Applicant, ApplicantAdmin)

# admin.site.register(Student, StudentAdmin)

admin.site.register(Studentcourse)

admin.site.register(Education)

admin.site.register(Contactdetails)

admin.site.register(Tsessions)

admin.site.register(Questionnaire)

admin.site.register(Employee)
 