from django.urls import path

from . import views

urlpatterns = [
    path('pantry', views.pantry_view, name='pantry'),
]