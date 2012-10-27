from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = patterns(
    'contacts.views',
    url(r'^$', 'index'),
    url(r'^(?P<contact_id>\d+)/$', 'detail'),
    url(r'^(?P<contact_id>\d+)/edit/$', 'edit'),
    url(r'^sign_in/$', 'sign_in'),
    url(r'^sign_out/$', 'sign_out'),
    url(r'^statistics/$', 'statistics'),
)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
