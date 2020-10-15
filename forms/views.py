from django.shortcuts import render
from forms.models import StudentCard

def home(request):
	cards = StudentCard.objects.all()
	return render(request, 'forms/home.html', {'cards': cards})