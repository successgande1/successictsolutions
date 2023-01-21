from django.contrib import admin

from . models import *

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'message', 'date')
    list_per_page = 20

# Register your models here
admin.site.register(Contact, ContactAdmin)
