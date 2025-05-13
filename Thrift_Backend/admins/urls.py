from django.urls import path
from . import views

urlpatterns = [
	path('register/', views.register),
	path('getAdmins/', views.get_admins)
]