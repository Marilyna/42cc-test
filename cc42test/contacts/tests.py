from django.utils import unittest
from django.test.client import Client

from contacts import models, forms


class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        response = self.client.get('/1/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/10000/')
        self.assertEqual(response.status_code, 404)

    def test_edit_get(self):
        response = self.client.get('/1/edit/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('contacts/edit.html' in response.templates[0].name)

    def test_edit_post(self):
        response = self.client.post('/1/edit/')
        self.assertEqual(response.status_code, 200)

    def test_statistics(self):
        response = self.client.get('/statistics/')
        self.assertEqual(response.status_code, 200)

    def test_sign_in_get(self):
        response = self.client.get('/sign_in/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('contacts/sign_in.html' in response.templates[0].name)

    def test_sign_in_post(self):
        response = self.client.post('/sign_in/', {'login': 'admin',
                                                  'password': 'admin'})
        # 302 - redirect
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/sign_in/', {'login': 'wrong',
                                                  'password': 'wrong'})
        self.assertEqual(response.status_code, 200)

    def test_sign_out(self):
        response = self.client.get('/sign_out/')
        # 302 - redirect
        self.assertEqual(response.status_code, 302)


class MiddlewareTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_middleware(self):
        response = self.client.get('/')
        req = models.Request.objects.latest('id')
        self.assertEqual(req.url, '/')
        self.assertEqual(req.method, 'GET')


class ContextProcessorTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_context_processor(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('ADMINS' in response.context)
        self.assertEqual(response.context['STATIC_URL'], '/static/')


class FormsTest(unittest.TestCase):
    def test_login_form(self):
        correct_form_data = {'login': 'admin', 'password': 'admin'}
        form = forms.LoginForm(correct_form_data)
        self.assertTrue(form.is_valid())
        wrong_form_data = {'login': 'wrong', 'password': 'wrong'}
        form = forms.LoginForm(wrong_form_data)
        self.assertFalse(form.is_valid())
