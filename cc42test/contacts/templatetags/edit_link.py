from django import template
from django.core.urlresolvers import reverse


register = template.Library()


@register.simple_tag
def edit_link(instance):
    info = instance._meta.app_label, instance._meta.module_name
    name = 'admin:%s_%s_change' % info
    return reverse(name, args=[instance.pk])
