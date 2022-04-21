from django.urls import path

from . import views

urlpatterns = [
   # path('analytics', views.fitness_analytics_view, name='fitness_analytics'),
    path('analytics/add', views.analytics_add, name='analytics_add'),
    path('analytics/delete/<int:id>', views.analytics_delete, name='analytics_delete'),
    path('analytics/deleteall', views.analytics_deleteall, name='analytics_deleteall'),
    #path('analytics/calculatecalories', views.analytics_calculatecalories, name='analytics_calculatecalories')
]
