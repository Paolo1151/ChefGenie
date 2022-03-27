from django.shortcuts import render, reverse, redirect

from chefgenie.settings import BASE_DIR

from .forms import SearchForm
from .models import Recipe, Requirement
from .search_engine.nlpmodel import NLPModel

def recipe_home(request):
    return render(request, 'recipe/recipehome.html')


def recipe_recommend(request):
    model = NLPModel.load_model()
    form = SearchForm(request.POST)

    if form.is_valid():
        prompt = form.cleaned_data.get('search_term')  
        request.session['prompt'] = prompt
        request.session['recommendations'] = model.generate_recommendations(prompt)

    return redirect('recipe_results')

def recipe_results(request):
    if 'recommendations' in request.session:
        return render(request, 'recipe/reciperesults.html')
    else:
        return redirect('recipe_home')

def recipe_details(request, pk):
    recipe = Recipe.objects.get(id=pk)
    recipe_tags = list(recipe.tags.split(" "))
    recipe_ingredients = Requirement.objects.select_related('recipe').select_related('ingredient').filter(recipe_id = recipe.id)
    recipe_steps = list(recipe.steps.split(" | "))
    return render(
        request, 'recipe/recipedetails.html',
        {'recipe': recipe, 'recipe_tags': recipe_tags,
        'recipe_ingredients': recipe_ingredients, 'recipe_steps': recipe_steps}
    )




