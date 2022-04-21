from django import forms
from .models import RecipeReview, Mealmade

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
