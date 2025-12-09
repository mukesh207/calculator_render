from django.urls import path
from . import views

app_name = 'calculator'

urlpatterns = [
    path('', views.calculator_view, name='home'),
    path('calculate/', views.calculate_view, name='calculate'),
    path('history/', views.history_view, name='history'),
    path('history/clear/', views.clear_history_view, name='clear_history'),
]
