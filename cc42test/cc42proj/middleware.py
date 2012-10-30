from datetime import datetime
from django.core.urlresolvers import resolve

from contacts.models import Request
from contacts import views


class SaveRequestsMiddleware(object):
    PRIORITY_VIEWS = set([views.detail, views.edit])

    def process_request(self, request):
        req = Request()
        req.url = request.path_info
        if resolve(req.url).func in self.PRIORITY_VIEWS:
            req.priority = True
        req.method = request.method
        req.save()
        return None
