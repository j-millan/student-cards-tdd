from django.test import TestCase
from django.urls import reverse, resolve

from model_bakery import baker
from forms.models import StudentCard
from forms.forms import StudentForm

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