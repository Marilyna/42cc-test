from contacts.models import Request
from datetime import datetime

class SaveRequestsMiddleware(object):
    def process_request(self, request):
        req = Request()
        req.url = request.path_info
        req.method = request.method
        req.save()
        return None