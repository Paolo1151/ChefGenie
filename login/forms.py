from django import forms

from .models import Account, UserAccount


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'password', 'class': 'input_field'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'confirm password', 'class': 'input_field'
    }))

    class Meta:
        model = Account
        fields = ['email_address', 'username', 'password']

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match."
            )

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['email_address'].widget.attrs = {'placeholder': 'email address', 'class': 'input_field'}
        self.fields['username'].widget.attrs = {'placeholder': 'username', 'class': 'input_field'}

class EditAccountForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ['weight', 'height', 'weight_goal', 'calorie_goal', 'profile_picture']

    def clean(self):
        cleaned_data = super(EditAccountForm, self).clean()

    def __init__(self, *args, **kwargs):
        super(EditAccountForm, self).__init__(*args, **kwargs)


class LoginForm(forms.ModelForm):
    class Meta:
        model = Account 
        fields= ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'placeholder': 'username', 'class': 'input_field'}
        self.fields['password'].widget=forms.PasswordInput(attrs = {'placeholder': 'password', 'class': 'input_field'})