from django.utils import unittest
from django.test.client import Client
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse


from contacts import models, forms
from contacts.templatetags.edit_link import edit_link


class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_index(self):
        response = self.client.get(reverse('contacts.views.index'))
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        response = self.client.get(reverse('contacts.views.detail', args=(1,)))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('contacts.views.detail',
                                           args=(10000,)))
        self.assertEqual(response.status_code, 404)

    def test_edit_get(self):
        response = self.client.get(reverse('contacts.views.edit', args=(1,)))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('contacts/edit.html' in response.templates[0].name)

    def test_edit_post(self):
        response = self.client.post(reverse('contacts.views.edit', args=(1,)))
        self.assertEqual(response.status_code, 200)

    def test_statistics(self):
        response = self.client.get(reverse('contacts.views.statistics'))
        self.assertEqual(response.status_code, 200)

    def test_sign_in_get(self):
        response = self.client.get(reverse('contacts.views.sign_in'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('contacts/sign_in.html' in response.templates[0].name)

    def test_sign_in_post(self):
        response = self.client.post(reverse('contacts.views.sign_in'),
                                    {'login': 'admin', 'password': 'admin'})
        # 302 - redirect
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('contacts.views.sign_in'),
                                    {'login': 'wrong', 'password': 'wrong'})
        self.assertEqual(response.status_code, 200)

    def test_sign_out(self):
        response = self.client.get(reverse('contacts.views.sign_out'))
        # 302 - redirect
        self.assertEqual(response.status_code, 302)


class MiddlewareTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_middleware(self):
        response = self.client.get(reverse('contacts.views.index'))
        req = models.Request.objects.latest('id')
        self.assertEqual(req.url, reverse('contacts.views.index'))
        self.assertEqual(req.method, 'GET')
        self.assertFalse(req.priority)
        response = self.client.get(reverse('contacts.views.edit', args=(1,)))
        req = models.Request.objects.latest('id')
        self.assertEqual(req.url, reverse('contacts.views.edit', args=(1,)))
        self.assertEqual(req.method, 'GET')
        self.assertTrue(req.priority)


class ContextProcessorTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_context_processor(self):
        response = self.client.get(reverse('contacts.views.index'))
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


class TemplateTagsTest(unittest.TestCase):
    def test_edit_link(self):
        obj = models.Contact.objects.get(pk=1)
        self.assertEqual(edit_link(obj), '/admin/contacts/contact/1/')


class ModelLogTest(unittest.TestCase):
    def test_model_log(self):
        ctype = ContentType.objects.get_for_model(models.Request)
        req = models.Request(url='url', method='HEAD', )
        req.save()
        modellog = models.ModelLog.objects.latest('id')
        self.assertEqual(modellog.content_type, ctype)
        self.assertEqual(modellog.action, 'C')

        req.url = 'another-url'
        req.save()
        modellog = models.ModelLog.objects.latest('id')
        self.assertEqual(modellog.content_type, ctype)
        self.assertEqual(modellog.action, 'U')

        req.delete()
        modellog = models.ModelLog.objects.latest('id')
        self.assertEqual(modellog.content_type, ctype)
        self.assertEqual(modellog.action, 'D')
