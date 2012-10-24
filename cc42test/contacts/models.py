from django.db import models

# Create your models here.
class Contact (models.Model):
    name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    birth_date = models.DateField()
    bio = models.TextField()
    email = models.EmailField()
    jabber = models.EmailField()
    skype = models.CharField(max_length=20)
    other_contacts = models.TextField()
    
    def __unicode__(self):
        return self.name + ' ' +self.last_name

        
class Request (models.Model):
    url = models.CharField(max_length=100)
    method = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now=True)