from django import template
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType


register = template.Library()


@register.simple_tag
def edit_link(instance):
    contenttype = ContentType.objects.get_for_model(instance)
    info = contenttype.app_label, contenttype.model
    name = 'admin:%s_%s_change' % info
    return reverse(name, args=[instance.pk])
