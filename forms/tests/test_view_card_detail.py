from django.test import TestCase
from django.urls import reverse, resolve

from model_bakery import baker
from forms.models import StudentCard
from forms.forms import StudentForm
from forms.views import StudentCardDetailView

class StudentCardDetailViewTests(TestCase):
	def setUp(self):
		self.card = baker.make(StudentCard)
		self.url = reverse('forms:card_detail', kwargs={'pk': 1})
		self.response = self.client.get(self.url)

	def test_successful_status_code(self):
		self.assertEqual(self.response.status_code, 200)

	def test_url_resolves_correct_view_function(self):
		view = resolve(self.url)
		self.assertEqual(view.func.view_class, StudentCardDetailView)

	def test_template_used(self):
		self.assertTemplateUsed(self.response, 'forms/card_detail.html')

	def test_context_object(self):
		obj = self.response.context.get('card')
		self.assertIsInstance(obj, StudentCard)

	def test_renders_object_info(self):
		self.assertContains(self.response, self.card.first_name)