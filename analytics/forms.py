from django import forms
from recipe.models import Recipe
from .models import Mealmade

class AddMealmade(forms.ModelForm):
    recipename = forms.ModelChoiceField(queryset=Recipe.objects.all())
    class Meta:
        model = Mealmade
        fields = ['amount', 'calories']

        