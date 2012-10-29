from django.db import models
from django.contrib.contenttypes.models import ContentType


class Contact(models.Model):
    name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    birth_date = models.DateField()
    bio = models.TextField()
    email = models.EmailField()
    jabber = models.EmailField()
    skype = models.CharField(max_length=20)
    other_contacts = models.TextField()
    photo = models.ImageField(upload_to='photos', null=True, blank=True)

    def __unicode__(self):
        return self.name + ' ' + self.last_name


class Request(models.Model):
    url = models.CharField(max_length=100)
    method = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now=True)


class ModelLog(models.Model):
    # handicapped CRUD
    CUD = (
        (u'C', u'Create'),
        (u'U', u'Update'),
        (u'D', u'Delete'),
    )
    content_type = models.ForeignKey(ContentType, related_name='+')
    action = models.CharField(max_length=1, choices=CUD)
    timestamp = models.DateTimeField(auto_now=True)
