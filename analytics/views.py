# Create your views here.

from django.shortcuts import render, redirect

from .models import Mealmade
from login.models import User as Profile
from .forms import AddMealmade


def fitness_analytics_view(request):
	'''
    Defines the view of the pantry page.

    Parameters
    -----------
    request: a request object from django

    Returns
    -----------
    rendered: A Rendered Page Object based on the html
    '''
	user = Profile.objects.get(id =request.session['user_index'])
	log = Mealmade.objects.values_list('calories', 'amount')
	#print(user.calorie_goal)
	total_calories = 0
	for a in log:
		total_calories += (a[0] * a[1])
	calorie_goal_status = user.calorie_goal - total_calories
	
	context = {
		'calorie_goal' : user.calorie_goal,
		'calorie_goal_status' : calorie_goal_status,
		'analytics': Mealmade.objects.all(),
		'add_form': AddMealmade(),
	}

	return render(request, 'analytics/analytics.html', context )

def analytics_add(request):
	'''
	Defines the Adding of a new unique pantry entry

	Parameters
	----------
	request: a request object from django

	Returns
	----------
	a redirect to the gallery view
	'''
	form = AddMealmade(request.POST, request.FILES)
	if form.is_valid():
		new_meal = Mealmade(
			recipename = form.cleaned_data['recipename'],
			amount = form.cleaned_data['amount'],
			calories = form.cleaned_data['calories']
		)
		new_meal.save()
	return redirect('fitness_analytics')

def analytics_deleteall(request):
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
	Mealmade.objects.all().delete()
	return redirect('fitness_analytics')

def analytics_delete(request, id):
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
	to_delete_obj = Mealmade.objects.get(id=id)
	to_delete_obj.delete()
	return redirect('fitness_analytics')

""" def analytics_calculatecalories(request, id):
	'''
    Defines the view of the pantry page.

    Parameters
    -----------
    request: a request object from django

    Returns
    -----------
    rendered: A Rendered Page Object based on the html
    '''
	user = Profile.objects.get(id =request.session['user_index'])
	total_calories = 0
	for a in Mealmade.objects.values_list('calories'):
		total_calories += a

	calorie_goal_status = user.calorie_goal - total_calories

	context = {
		'calorie_goal' : user.calorie_goal,
		'calorie_goal_status' : calorie_goal_status

	}

	return redirect('fitness_analytics', context) """