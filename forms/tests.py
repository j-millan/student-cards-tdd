from django.test import TestCase
from django.urls import reverse, resolve

from model_bakery import baker
from forms.models import StudentCard
from forms.forms import StudentForm
from forms.views import home, StudentFormView

class HomeViewTests(TestCase):
	def setUp(self):
		self.card = baker.make(StudentCard)
		self.home_url = reverse('forms:home')
		self.response = self.client.get(self.home_url)

	def test_view_sucessful_status_code(self):
		self.assertEqual(self.response.status_code, 200)

	def test_url_resolves_correct_view_function(self):
		view = resolve(self.home_url)
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

class StudentFormViewTests(TestCase):
	def setUp(self):
		self.card = baker.make(StudentCard)
		self.data = self.card.__dict__
		self.card.delete()
		self.data.pop('id')

		self.student_form_url = reverse('forms:student_form')
		self.response = self.client.get(self.student_form_url)

	def test_view_successful_status_code(self):
		self.assertEqual(self.response.status_code, 200)

	def test_url_resolves_correct_view(self):
		view = resolve(self.student_form_url)
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

	def test_successful_post_request(self):
		response = self.client.post(self.student_form_url, self.data)

		home_url = reverse('forms:home')
		self.assertTrue(StudentCard.objects.exists())
		self.assertRedirects(response, home_url)

	def test_empty_fields_form_request(self):
		response = self.client.post(self.student_form_url, {})
		form = response.context.get('form')
		self.assertTrue(form.errors)
		self.assertEqual(response.status_code, 200)
		self.assertFalse(StudentCard.objects.exists())

	def test_invalid_form_request(self):
		data = self.data
		data['first_name'] = '1111111.....'
		data['last_name'] = '())..@'
		response = self.client.post(self.student_form_url)
		form = response.context.get('form')
		self.assertTrue(form.errors)
		self.assertEqual(response.status_code, 200)
		self.assertFalse(StudentCard.objects.exists())

class StudentCardModelTests(TestCase):
	def setUp(self):
		self.card1 = baker.make(StudentCard, first_name='Nick', last_name='Mason')
		self.card2 = baker.make(StudentCard, first_name='Dave')

	def test_created_properly(self):
		cards = StudentCard.objects.all()

		self.assertTrue(self.card1 in cards)
		self.assertTrue(self.card2 in cards)

		self.assertEqual(self.card1.first_name, 'Nick')
		self.assertEqual(self.card2.first_name, 'Dave')


	def test_str_method(self):
		self.assertEqual(self.card1.__str__(), 'Nick Mason')

class StudentFormTests(TestCase):
	def test_form_has_fields(self):
		form = StudentForm()
		expected = ['first_name', 'last_name', 'birth_date', 'country_of_origin', 'study', 'job']
		actual = list(form.fields)
		self.assertSequenceEqual(expected, actual)

	def test_valid_form(self):
		data = baker.make(StudentCard)
		form = StudentForm(data.__dict__)
		self.assertTrue(form.is_valid())