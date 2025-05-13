from django.urls import path
from . import views

urlpatterns = [
    path('makeOrder/', views.makeOrder),
    path('getOrders/', views.get_Orders),
]