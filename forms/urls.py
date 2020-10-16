from django.urls import path
from forms import views

app_name = 'forms'

urlpatterns = [
	path('', views.home, name='home'),
	path('form/', views.StudentFormView.as_view(), name='student_form'),
	path('card/<int:pk>/', views.StudentCardDetailView.as_view(), name='card_detail')
]