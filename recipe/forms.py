from django import forms

from .models import RecipeReview
from .models import Mealmade
from .models import UserPantry
from .models import Ingredient
from .models import Recipe

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

class AddRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'tags', 'ingredients', 'steps']
