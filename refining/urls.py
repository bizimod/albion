from django.urls import path
from .views import refining_calculation

urlpatterns = [
    path('calculator/', refining_calculation, name='refining_calculation'),
]