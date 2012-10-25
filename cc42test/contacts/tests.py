from django.utils import unittest
from django.test.client import RequestFactory
from django.http import Http404

from contacts import views
from cc42proj import middleware, context_processors

class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()
         
    def test_index(self):
        request = self.factory.get('/')
        response = views.index(request)
        self.assertEqual(response.status_code, 200)
        
    def test_detail(self):
        request = self.factory.get('/1/')
        response = views.detail(request, 1)
        self.assertEqual(response.status_code, 200)

        request = self.factory.get('/10000/')
        try:
            response = views.detail(request, 10000)
        except Http404:
            pass
        else:
            self.fail()
            
    def test_statistic(self):
        request = self.factory.get('/statistic/')
        response = views.statistic(request)
        self.assertEqual(response.status_code, 200)

        
class MiddlewareTest(unittest.TestCase):
    def setUp(self):
        self.mw = middleware.SaveRequestsMiddleware()
        self.factory = RequestFactory()

    def test_middleware(self):
        request = self.factory.get('/')
        self.assertEqual(self.mw.process_request(request), None)
        
        
class ContextProcessorTest(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        
    def test_context_processor(self):
        request = self.factory.get('/')
        result = context_processors.save_django_settings(request)
        self.assertTrue(isinstance(result, dict))