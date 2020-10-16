from django.test import TestCase
from django.urls import reverse, resolve

from model_bakery import baker
from forms.models import StudentCard
from forms.forms import StudentForm
from forms.views import StudentFormView

class StudentFormViewTestCase(TestCase):
	def setUp(self):
		self.url = reverse('forms:student_form')
		self.card = baker.make(StudentCard)
		self.data = self.card.__dict__
		self.card.delete()
		self.data.pop('id')

class StudentFormViewTests(TestCase):
	def setUp(self):
		super().setUp()
		self.url = reverse('forms:student_form')
		self.response = self.client.get(self.url)

	def test_view_successful_status_code(self):
		self.assertEqual(self.response.status_code, 200)

	def test_url_resolves_correct_view_function(self):
		view = resolve(self.url)
		self.assertEqual(view.func.view_class, StudentFormView)

	def test_template_used(self):
		self.assertTemplateUsed(self.response, 'forms/student_form.html')

	def test_contains_form(self):
		form = self.response.context.get('form')
		self.assertIsInstance(form, StudentForm)

	def test_csrf(self):
		self.assertContains(self.response, 'csrfmiddlewaretoken')

	def test_form_inputs(self):
		self.assertContains(self.response, '<input type="text"', 2)
		self.assertContains(self.response, '<input type="checkbox"', 1)
		self.assertContains(self.response, '<select', 2)
		self.assertContains(self.response, '<input type="date"', 1)
		self.assertContains(self.response, 'type="submit"', 1)

class StudentFormViewSuccessfulPostRequestTests(StudentFormViewTestCase):
	def setUp(self):
		super().setUp()
		self.response = self.client.post(self.url, self.data)


	def test_object_created(self):
		self.assertTrue(StudentCard.objects.exists())

	def test_redirection(self):
		home_url = reverse('forms:home')
		self.assertRedirects(self.response, home_url)

class StudentFormViewInvalidPostRequest(StudentFormViewTestCase):
	def setUp(self):
		super().setUp()
		data = self.data
		data['first_name'] = '1111111.....'
		data['last_name'] = '())..@'
		self.response = self.client.post(self.url)

	def test_object_not_created(self):
		self.assertFalse(StudentCard.objects.exists())
		
	def test_form_errors(self):
		form = self.response.context.get('form')
		self.assertTrue(form.errors)

	def test_redirection(self):
		self.assertEqual(self.response.status_code, 200)

class StudentFormViewEmptyFieldsRequest(StudentFormViewTestCase):
	def setUp(self):
		super().setUp()
		self.response = self.client.post(self.url, {})

	def test_object_not_created(self):
		self.assertFalse(StudentCard.objects.exists())
		
	def test_form_errors(self):
		form = self.response.context.get('form')
		self.assertTrue(form.errors)

	def test_redirection(self):
		self.assertEqual(self.response.status_code, 200)