from django.shortcuts import render, redirect

from .models import Ingredients
from .forms import AddIngredientForm


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
	return render(request, 'pantry/pantry.html', {
		'pantry': Ingredients.objects.all().order_by('id'),
		'add_form': AddIngredientForm()
	})


def pantry_add(request):
	'''
	Defines the Adding of a new unique pantry entry

	Parameters
	----------
	request: a request object from django

	Returns
	----------
	a redirect to the gallery view
	'''
	form = AddIngredientForm(request.POST, request.FILES)
	if form.is_valid():
		new_ingr = Ingredients(
			img = form.cleaned_data['img'],
			name = form.cleaned_data['name'],
			amount = form.cleaned_data['amount']
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
	to_delete_obj = Ingredients.objects.get(id=id)
	to_delete_obj.delete()
	return redirect('pantry_home')


def pantry_quantity_add(request, id):
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
	to_update = Ingredients.objects.get(id=id)
	to_update.amount += 1
	to_update.save()
	return redirect('pantry_home')



