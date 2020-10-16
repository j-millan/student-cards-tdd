from django.db import models
from django_countries.fields import CountryField

class StudentCard(models.Model):
	STUDIES_LIST = [
		('PH', 'Physics'),
		('CH', 'Chemistry'),
		('ME', 'Medicine'),
		('ML', 'Modern languages'),
		('MS', 'Music'),
		('VA', 'Visual arts'),
		('GD', 'Graphic design'),
		('MC', 'Mechanical engineering'),
		('CO', 'COmputing')
	]

	first_name = models.CharField(max_length=65)
	last_name = models.CharField(max_length=65)
	birth_date = models.DateField(auto_now=False, auto_now_add=False)
	country_of_origin = CountryField()
	study = models.CharField(max_length=35,choices=STUDIES_LIST)
	job = models.BooleanField()

	def get_full_name(self):
		return f'{self.first_name} {self.last_name}'

	def __str__(self):
		return self.get_full_name()