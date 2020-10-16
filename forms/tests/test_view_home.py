from django.test import TestCase
from django.urls import reverse, resolve

from model_bakery import baker
from forms.models import StudentCard
from forms.views import home, StudentFormView

class HomeViewTests(TestCase):
	def setUp(self):
		self.card = baker.make(StudentCard)
		self.url = reverse('forms:home')
		self.response = self.client.get(self.url)

	def test_view_sucessful_status_code(self):
		self.assertEqual(self.response.status_code, 200)

	def test_url_resolves_correct_view_function(self):
		view = resolve(self.url)
		self.assertEqual(view.func, home)

	def test_template_used(self):
		self.assertTemplateUsed(self.response, 'forms/home.html')

	def test_context_contains_student_cards(self):
		self.assertTrue(self.response.context.get('cards'))

	def test_renders_student_cards(self):
		self.assertContains(self.response, f'{self.card.first_name} {self.card.last_name}')

	def test_contains_link_to_user_form_view(self):
		student_form_url = reverse('forms:student_form')
		self.assertContains(self.response, 'href="{0}"'.format(student_form_url))