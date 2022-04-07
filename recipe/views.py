from django.shortcuts import render, reverse, redirect
from django.contrib import messages

from chefgenie.settings import BASE_DIR, NLP_MODEL

from .forms import SearchForm, ReviewForm
from .models import Recipe, Requirement, RecipeReview
from .search_engine.nlpmodel import NLPModel
from .search_engine.filters import SearchConfig


import psycopg2

def recipe_home(request):
    return render(request, 'recipe/recipehome.html')


def recipe_recommend(request):
    form = SearchForm(request.POST)

    # Generate Search Config
    if 'filter_enabled' in request.POST:
        search_config = SearchConfig.create_new(request.POST)
    else:
        search_config = None

    # Check if the Search Term is Valid
    if form.is_valid():
            prompt = form.cleaned_data.get('search_term')  
            request.session['prompt'] = prompt
            request.session['recommendations'] = NLP_MODEL.generate_recommendations(prompt, search_config)

    # Redirect to the Recipe Results
    return redirect('recipe_results')


def recipe_results(request):
    if 'recommendations' in request.session:
        return render(request, 'recipe/reciperesults.html')
    else:
        return redirect('recipe_home')

# Displaying individual Recipe pages
def recipe_details(request, pk):
    recipe = Recipe.objects.get(id=pk)
    recipe_tags = list(recipe.tags.split(" "))
    recipe_ingredients = Requirement.objects.select_related('recipe').select_related('ingredient').filter(recipe_id = recipe.id)
    recipe_steps = list(recipe.steps.split(" | "))
    reviews = RecipeReview.objects.all().filter(recipe__id=pk).values('user__user__username', 'rating', 'comment')
    return render(
        request, 'recipe/recipedetails.html', {
            'recipe': recipe,
            'recipe_tags': recipe_tags,
            'recipe_ingredients': recipe_ingredients,
            'recipe_steps': recipe_steps,
            'reviews': reviews
        }
    )

def submit_review(request, recipe_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            review = RecipeReview.objects.get(user__id=request.user.id, recipe__id=recipe_id)
            form = ReviewForm(request.POST, instance=review)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except RecipeReview.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = RecipeReview()
                data.rating = form.cleaned_data['rating']
                data.comment = form.cleaned_data['comment']
                data.recipe_id = recipe_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been posted.')
                return redirect(url)

