from django.urls import path
from forms import views

app_name = 'forms'

urlpatterns = [
	path('', views.home, name='home')
]