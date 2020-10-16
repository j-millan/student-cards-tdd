from django.shortcuts import render, redirect
from django.views.generic import FormView

from forms.models import StudentCard
from forms.forms import StudentForm

def home(request):
	cards = StudentCard.objects.all()
	return render(request, 'forms/home.html', {'cards': cards})

class StudentFormView(FormView):
	model = StudentCard
	form_class = StudentForm
	template_name = "forms/student_form.html"

	def form_valid(self, form):
		form.save()
		return redirect('forms:home')