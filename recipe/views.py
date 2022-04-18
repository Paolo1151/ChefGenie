from django.shortcuts import render, reverse, redirect
from django.contrib import messages

from chefgenie.settings import BASE_DIR, NLP_MODEL

from .forms import SearchForm, ReviewForm
from .models import Recipe, Requirement, RecipeReview
from .search_engine.nlpmodel import NLPModel
from .search_engine.filters import SearchConfig

from analytics.models import Mealmade


import psycopg2

def recipe_home(request):
    '''
    Render the Home page of the Recipes HTML
    
    request : Django Request object
        Request is assumed to be a GET protocol 
    '''
    return render(request, 'recipe/recipehome.html')


def recipe_recommend(request):
    '''
    Render the Recipe Recommendation based on the prompt.

    Parameters
    ----------
    request : django request object
        Contains
            - prompt : a text from the search bar
            - filters: parameters for filters to be parsed in
                the creation of a search config
        
    Returns
    -----------
    a redirect to the recipe_results url

    '''
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
    '''Render the recommendations if it exists'''
    if 'recommendations' in request.session:
        return render(request, 'recipe/reciperesults.html')
    else:
        return redirect('recipe_home')

# Displaying individual Recipe pages
def recipe_details(request, pk):
    '''
    Display the details of the clicked recipe

    Parameters
    ----------
    pk : int
        The id of the related object that is to be shown

    Returns
    ----------
    a rendered webpage that has the details of the recipe

    '''
    recipe = Recipe.objects.get(id=pk)
    return render(
        request, 'recipe/recipedetails.html', {
            'recipe': recipe,
            'recipe_tags': recipe.tags.split(" "),
            'recipe_ingredients': Requirement.objects.select_related('recipe').select_related('ingredient').filter(recipe_id=recipe.id),
            'recipe_steps': recipe.steps.split(" | "),
            'reviews': RecipeReview.objects.filter(recipe__id=pk).values('user__user__username', 'rating', 'comment')
        }
    )

def make_recipe(request, pk):
    user_id = request.user.id

    # Record the new recipe with the user id

    pass

def submit_review(request, recipe_id):
    '''
    Submit a user review about the chosen recipe

    Parameters
    ----------
    recipe_id : int
        the id of the recipe that is to be reviewed

    Returns
    --------
    a redirect to the previous page
    
    '''
    url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        try:
            review = RecipeReview.objects.get(user__id=request.user.id, recipe__id=recipe_id)
            form = ReviewForm(request.POST, instance=review)
            form.save()
            
            messages.success(request, 'Thank you! Your review has been updated.')
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
