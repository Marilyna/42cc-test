from django.utils import unittest
from django.test.client import RequestFactory
from django.http import Http404

from contacts import views

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