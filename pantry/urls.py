from django.urls import path

from . import views

urlpatterns = [
    path('pantry', views.pantry_gallery_view, name='pantry_home'),
    path('pantry/add', views.pantry_add, name='pantry_add'),
    path('pantry/delete/<int:id>', views.pantry_delete, name='pantry_delete'),
    path('pantry/qadd/<int:id>', views.pantry_quantity_add, name='pantry_qadd')
]