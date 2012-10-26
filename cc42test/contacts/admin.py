from contacts.models import Contact, Request
from django.contrib import admin

class ContactAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Personal info', {'fields': ['name', 'last_name', 'birth_date']}),
        ('Contacts', {'fields': ['email', 'jabber', 'skype', 'other_contacts']}),
        ('Other', {'fields': ['bio']}),
        ('Photo', {'fields': ['photo']})
    ]

class RequestAdmin(admin.ModelAdmin):
    list_display = ('url', 'method', 'timestamp')
    
admin.site.register(Contact, ContactAdmin)
admin.site.register(Request, RequestAdmin)