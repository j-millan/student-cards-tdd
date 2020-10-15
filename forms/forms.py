from django import forms
from forms.models import StudentCard

class StudentForm(forms.ModelForm):
    class Meta:
        model = StudentCard
        fields = ('__all__')
