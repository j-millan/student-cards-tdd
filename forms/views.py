from django.shortcuts import render, redirect
from django.views.generic import FormView, DetailView

from forms.models import StudentCard
from forms.forms import StudentForm

class StudentCardDetailView(DetailView):
    model = StudentCard
    context_object_name = 'card'
    template_name = "forms/card_detail.html"

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