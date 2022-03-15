from django.urls import path

from .views import recipe_home, recipe_recommend, recipe_results

urlpatterns = [
    path('recipe', recipe_home, name='recipe_home'),
    path('recipe/recommend', recipe_recommend, name='recipe_recommend'),
    path('recipe/search_results', recipe_results, name='recipe_results')
]