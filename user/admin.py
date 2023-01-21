from django.contrib import admin
from . models import * 

# Register your models here.

#Register Admin Profile Table
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'surname', 'othernames', 'gender', 'phone', 'image')
    list_per_page = 25
#Register Profile Table
admin.site.register(Profile, ProfileAdmin)

#Register Admin Course Table
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'form_fee', 'course_fee', 'logo', 'added_date')
    list_per_page = 25
#Register Course Table
admin.site.register(Course, CourseAdmin)
