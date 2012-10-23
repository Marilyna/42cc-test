from cc42test.contacts.models import Contact
#from contacts.models import Contact
from django.contrib import admin

class ContactAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Personal info', {'fields': ['name', 'last_name', 'birth_date']}),
        ('Contacts', {'fields': ['email', 'jabber', 'skype', 'other_contacts']}),
        ('Other', {'fields': ['bio']})
    ]

admin.site.register(Contact, ContactAdmin)