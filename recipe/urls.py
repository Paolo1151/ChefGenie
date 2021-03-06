from django.urls import path

from . import views

urlpatterns = [
    path('home/<str:recom_type>', views.home, name='home'),

    path('recipe', views.recipe_home, name='recipe_home'),
    path('recipe/recommend', views.recipe_recommend, name='recipe_recommend'),
    path('recipe/search_results', views.recipe_results, name='recipe_results'),
    path('recipe/<int:pk>', views.recipe_details, name='recipe_details'),
    path('recipe/make/<int:pk>', views.make_recipe, name='make_recipe'),
    path('recipe/add', views.recipe_add, name='recipe_add'),
    path('recipe/add2', views.recipe_add2, name='recipe_add2'),
    path('recipe/add3', views.recipe_add3, name='recipe_add3'),

    path('submit_review/<int:recipe_id>', views.submit_review, name='submit_review'),

    path('analytics', views.analytics_home, name='analytics'),

    path('pantry', views.pantry_gallery_view, name='pantry_home'),
    path('pantry/add', views.pantry_add, name='pantry_add'),
    path('pantry/delete/<int:id>', views.pantry_delete, name='pantry_delete'),
]