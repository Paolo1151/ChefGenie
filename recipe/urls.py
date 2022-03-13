from django.urls import path

from .views import recipe_home, recipe_recommendations

urlpatterns = [
    path('recipe', recipe_home, name='recipe_home'),
    path('recipe/recommendations/<str:search_term>', recipe_recommendations, name='recipe_recommend')
]