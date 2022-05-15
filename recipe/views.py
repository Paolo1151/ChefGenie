from django.shortcuts import render
from django.shortcuts import reverse
from django.shortcuts import redirect

from django.conf import settings

from django.contrib import messages
from django.contrib.auth import get_user_model

from .forms import SearchForm
from .forms import ReviewForm
from .forms import MealmadeForm
from .forms import AddIngredientForm
from .forms import AddRecipeForm

from .models import Recipe
from .models import Requirement
from .models import RecipeReview
from .models import Mealmade
from .models import Ingredient
from .models import UserPantry

from login.models import UserAccount

from .utils import search
from .utils.search.config import SearchConfig
from .utils import analytics


def home(request, recom_type):
    recomms = settings.RECOM_ENGINE.generate_recommendations(5, recom_type, request.user.id)

    user = UserAccount.objects.get(user_id=request.user.id)
    context = {
        'account': get_user_model().objects.get(id=request.user.id),
        'user': user,
        'weightGoalMet': user.weight == user.weight_goal,
        'weightBelowGoal': user.weight < user.weight_goal,
        'weightDifference': abs(user.weight_goal - user.weight),
        'calories_consumed': user.calorie_goal - settings.SEARCH_ENGINE.calculate_calorie_goal(user),
        'recommendations': recomms,
        'recom_type': recom_type
    }
    return render(request, 'home/home.html', context)


def recipe_home(request):
    '''
    Render the Home page of the Recipes HTML
    
    request : Django Request object
        Request is assumed to be a GET protocol 
    '''
    if request.user.id is not None:
        return render(request, 'recipe/recipehome.html')
    else:
        return redirect('login')


def analytics_home(request):
    '''
    Render the Home page of the Recipes HTML
    
    request : Django Request object
        Request is assumed to be a GET protocol 
    '''
    if request.user.id is not None:
        context = settings.ANALYTICS_ENGINE.graph_calorie_intake(request.user.id, 7)
        context['table'] = settings.ANALYTICS_ENGINE.table_calorie_intake(request.user.id, 7)
        return render(request, 'recipe/analytics.html', context)
    else:
        return redirect('login')


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
    search_config = SearchConfig.create_new(request.POST, UserAccount.objects.get(user_id=request.user.id))

    # Check if the Search Term is Valid
    if form.is_valid():
            prompt = form.cleaned_data.get('search_term')  
            request.session['prompt'] = prompt
            results = settings.SEARCH_ENGINE.generate_search_results(prompt, search_config)
            request.session['result_goal'] = results['goal_recipes']
            request.session['result_other'] = results['other_recipes']

    # Redirect to the Recipe Results
    return redirect('recipe_results')


def recipe_results(request):
    '''Render the recommendations if it exists'''
    if 'result_goal' in request.session and 'result_other' in request.session:
        return render(request, 'recipe/reciperesults.html')
    else:
        return redirect('recipe_home')


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
            'reviews': RecipeReview.objects.filter(recipe__id=pk).values('user__username', 'rating', 'comment')
        }
    )


def make_recipe(request, pk):
    url = request.META.get('HTTP_REFERER')
    request.session['is_insufficient'] = False
    recipe_id = pk
    if request.method == 'POST':
        form = MealmadeForm(request.POST)
        if form.is_valid():
            missing, to_update = settings.VALIDATOR.validate(pk, form.cleaned_data['amount'])
            if not missing:
                consume = Mealmade()
                consume.recipe_id = recipe_id
                consume.user_id = request.user.id
                consume.amount = form.cleaned_data['amount']
                consume.save()

                for rid, consumed in to_update:
                    ingredient = UserPantry.objects.get(ingredient__id=rid, user__id=request.user.id)
                    ingredient.amount -= consumed
                    ingredient.save()

                messages.success(request, 'Thank you! This meal has been added to your history.', extra_tags='meal')
            else:
                request.session['requirements'] = missing
                request.session['is_insufficient'] = True
                messages.warning(request, 'Insufficient Ingredients for Recipe!', extra_tags='meal')
    return redirect(url)


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
            
            messages.success(request, 'Thank you! Your review has been updated.', extra_tags='review')
        except RecipeReview.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = RecipeReview()
                data.rating = form.cleaned_data['rating']
                data.comment = form.cleaned_data['comment']
                data.recipe_id = recipe_id
                data.user_id = request.user.id
                data.save()

                messages.success(request, 'Thank you! Your review has been posted.', extra_tags='review')
    
    return redirect(url)


def pantry_gallery_view(request):
    '''
    Defines the view of the pantry page.

    Parameters
    -----------
    request: a request object from django

    Returns
    -----------
    rendered: A Rendered Page Object based on the html
    ''' 
    if request.user.id is not None:
        return render(request, 'pantry/pantry.html', {
            'pantry': UserPantry.objects.all().filter(user__id=request.user.id).order_by('id'),
            'add_form': AddIngredientForm()
        })
    else:
        return redirect('login')


def pantry_add(request):	
    '''
	Defines the Addition of a new Ingredient

	Parameters
	----------
	request: Django.request 
		a request object from django

	Returns
	----------
	a redirect to the gallery view
	'''
    form = AddIngredientForm(request.POST)
    if form.is_valid():
        new_ingr = UserPantry(
            ingredient=form.cleaned_data['ingredient'],
            user=request.user,
        )
        new_ingr.save()
    return redirect('pantry_home')


def pantry_delete(request, id):
    '''
	Defines the Deletion of a specific pantry entity

	Parameters
	----------
	request: Django.request 
		a request object from django
	id : int
		the id of the object concerned

	Returns
	----------
	a redirect to the gallery view
	'''
    to_delete_obj = UserPantry.objects.filter(id=id)
    to_delete_obj.delete()
    return redirect('pantry_home')

'''
# def pantry_quantity_add(request, id):

# 	Defines the Deletion of a specific pantry entity

# 	Parameters
# 	----------
# 	request: Django.request 
# 		a request object from django
# 	id : int
# 		the id of the object concerned

	Returns
	----------
	a redirect to the gallery view

    to_update = UserPantry.objects.get(id=id)
    to_update.amount += 1
    to_update.save()
    return redirect('pantry_home')

def recipe_add(request):
    if request.method == 'POST':
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            tags = form.cleaned_data['tags']
            ingredients = form.cleaned_data['ingredients']
            steps = form.cleaned_data['steps']
            recipe = Recipe.objects.create(name=name, tags=tags, steps=steps)
            # recipe.ingredients.set(ingredients)
            recipe.save()
            return redirect('/recipe')
        else:
                message = 'Details incomplete'
    else:
        message = ''
        form = AddRecipeForm()

    context = {'message': message, 'form': form}
    return render(request, 'recipe/recipeadd.html', context)
# 	Returns
# 	----------
# 	a redirect to the gallery view
# 	'''
#     to_update = UserPantry.objects.get(id=id)
#     to_update.amount += 1
#     to_update.save()
#     return redirect('pantry_home')
