from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('cats/<slug:cat_slug>/', views.categories_by_slug, name='category'),
]
