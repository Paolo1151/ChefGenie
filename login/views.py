from django.shortcuts import redirect, render
from django.http import HttpResponse

from .models import User
from .forms import LoginForm

def account_view(request):
    '''
    Defines the View of the Account Page after login.
    Only Accessible if user_index and user is populated.

    Parameters
    -----------
    request: a request object from django

    Returns
    -----------
    rendered: A Rendered Page based on a context
    '''
    return render(
        request, "account/account.html", {
        'user_index': request.session['user_index'],
        'user': User.objects.get(id=request.session['user_index'])
    })

def login_view(request):
    '''
    Defines the view of the login page.

    Parameters
    -----------
    request: a request object from django

    Returns
    -----------
    rendered: A Rendered Page Object based on the context
    '''

    context = {'error_message': ''}

    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            user = User.objects.all().get(
                        username=login_form.cleaned_data.get('username'),
                        password=login_form.cleaned_data.get('password')
                    )

            if user:
                request.session['user_index'] = user.pk
                return redirect('account')

        request.session['error_message'] = 'invalid username or password'

    return render(request, "login/login.html", context)

