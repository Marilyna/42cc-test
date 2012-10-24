from django.conf import settings

def save_django_settings(request):
    django_settings = {}
    for k in dir(settings):
        if not k.startswith('_'):
            django_settings[k] = getattr(settings, k)
    return django_settings