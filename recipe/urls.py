from django.urls import path

from .views import recipe_home, recipe_recommend, recipe_results, recipe_details, make_recipe, submit_review

urlpatterns = [
    path('recipe', recipe_home, name='recipe_home'),
    path('recipe/recommend', recipe_recommend, name='recipe_recommend'),
    path('recipe/search_results', recipe_results, name='recipe_results'),
    path('recipe/<int:pk>', recipe_details, name='recipe_details'),
    path('recipe/make/<int:pk>', make_recipe, name='make_recipe'),
    path('submit_review/<int:recipe_id>', submit_review, name='submit_review'),
]