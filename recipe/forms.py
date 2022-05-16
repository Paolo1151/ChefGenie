from django import forms

from .models import RecipeReview
from .models import Mealmade
from .models import UserPantry
from .models import Ingredient
from .models import Recipe
from .models import Requirement

class SearchForm(forms.Form):
    search_term = forms.CharField(label='Search Term')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = RecipeReview
        fields = ['rating', 'comment']


class MealmadeForm(forms.ModelForm):
    class Meta:
        model = Mealmade
        fields = ['amount']


class AddIngredientForm(forms.ModelForm):
    class Meta:
        model = UserPantry
        fields = ['ingredient']

    def __init__(self, *args, **kwargs):
        super(AddIngredientForm, self).__init__(*args, **kwargs)
        self.fields['ingredient'].widget.attrs = {'class': 'ingredient_input_field'}

class AddRecipeNameForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'tags']
    
    def __init__(self, *args, **kwargs):
        super(AddRecipeNameForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {'placeholder': 'recipe name', 'class': 'input_field'}
        self.fields['tags'].widget.attrs = {'placeholder': 'tags (separated by spaces)', 'class': 'input_field'}

class AddRequirementForm(forms.ModelForm):
    class Meta:
        model = Requirement
        fields = ['ingredient', 'required_amount']
    
    def __init__(self, *args, **kwargs):
        super(AddRequirementForm, self).__init__(*args, **kwargs)
        self.fields['ingredient'].widget.attrs = {'placeholder': 'ingredient', 'class': 'input_field'}
        self.fields['required_amount'].widget.attrs = {'placeholder': 'amount', 'class': 'input_field'}

class AddStepsForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['steps']
    
    def __init__(self, *args, **kwargs):
        super(AddStepsForm, self).__init__(*args, **kwargs)
        self.fields['steps'].widget.attrs = {'placeholder': 'enter steps separated by \'|\'', 'class': 'input_field'}