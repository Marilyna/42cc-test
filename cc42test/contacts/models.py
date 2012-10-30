from traceback import format_exc
from logging import getLogger

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.contrib.contenttypes.models import ContentType


log = getLogger('cc42test')


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
    priority = models.BooleanField()

    def date_time(self):
        return self.timestamp.strftime('%Y-%m-%d %H:%M:%S')


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

    @classmethod
    def record(cls, sender, action):
        if sender == cls:
            return
        try:
            ctype = ContentType.objects.get_for_model(sender)
            cls.objects.create(content_type=ctype, action=action)
        except Exception:
            log.error('Error on logging model change: %s', format_exc())

    @classmethod
    def post_save(cls, sender, created, **kwargs):
        cls.record(sender, 'C' if created else 'U')

    @classmethod
    def post_delete(cls, sender, **kwargs):
        cls.record(sender, 'D')


post_save.connect(ModelLog.post_save)
post_delete.connect(ModelLog.post_delete)
