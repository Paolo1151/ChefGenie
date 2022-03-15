from django import forms

from .models import User

class LoginForm(forms.ModelForm):
    class Meta:
        model = User 
        fields= ['username', 'password']

class SignupForm(forms.Form):
    email_address = forms.EmailField()
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)
    password_confirm = forms.CharField(max_length=255)