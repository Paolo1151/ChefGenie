from django import forms

from .models import Ingredients

class AddIngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredients
        fields = ['name', 'amount']