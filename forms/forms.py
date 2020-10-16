from django import forms
from forms.models import StudentCard

class StudentForm(forms.ModelForm):
	birth_date = forms.DateInput()

	class Meta:
		model = StudentCard
		fields = ('__all__')