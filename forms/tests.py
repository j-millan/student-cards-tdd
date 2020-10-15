from django.test import TestCase

from model_bakery import baker
from forms.models import StudentCard
from forms.forms import StudentForm

import datetime

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