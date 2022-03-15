from django.shortcuts import render
from .models import Ingredients
# Create your views here.

def pantry_view(request):
	pantry = Ingredients.objects.all()
	'''
    Defines the view of the pantry page.

    Parameters
    -----------
    request: a request object from django

    Returns
    -----------
    rendered: A Rendered Page Object based on the html
    '''
	if request.method == 'POST':
		if 'add' in request.POST:
			pantry_image = request.POST['pantry_image']
			pantry_name = request.POST['pantry_name']
			pantry_quantity= request.POST['pantry_quantity']
			
			insert_pantry = Ingredients(img = pantry_image, name=pantry_name, amount=pantry_quantity)
			insert_pantry.save()
		elif 'delete' in request.POST:
			pantry.filter(id=request.POST['pk']).delete()
		elif 'quantity_add' in request.POST:
			# to_be_added = pantry.objects.get(pk=request.POST['pk'])
			# to_be_added.amount += 
			# to_be_added.save()
			# pantry.filter(id=request.POST['pk']).update(amount = int(request.POST['amount']) + 1)
			to_be_added = Ingredients.objects.filter(id=request.POST['pk'])
			to_be_added.update(amount = int(request.POST['amount']) + 1)
			

	return render(request, 'pantry/pantry.html', {'pantry': pantry})



