from django.shortcuts import redirect, render
from django.http import HttpResponse

from .models import User
from .forms import LoginForm, SignupForm

def validate_signup(request_post):
    if request_post['password'] != request_post['password_confirm']:
        return 1
    elif User.objects.all().filter(username=request_post['username']).exists():
        return 2
    elif User.objects.all().filter(email_address=request_post['email_address']).exists():
        return 3
    else:
        return 0


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
    if 'user_index' not in request.session:
        request.session['user_index'] = 0

    try:
        user = User.objects.get(id=request.session['user_index'])
    except User.DoesNotExist:
        user = None

    return render(request, "login/account.html", {'user': user})


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
    context = {'message': ''}

    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            try:
                user = User.objects.get(
                            username=login_form.cleaned_data.get('username'),
                            password=login_form.cleaned_data.get('password')
                        )
            except User.DoesNotExist:
                user = None

            if user:
                request.session['user_index'] = user.pk
                return redirect('account')

        context['message'] = 'invalid username or password'
    return render(request, "login/login.html", context)


def signup_view(request):
    '''
    Defines the Signup view that allows users to signup for an account

    Parameters
    -----------
    request
        A request object that contains the request parameters

    Returns
    ----------
    rendered
        A new rendered webpage based on context
    '''
    context = {'message':''}

    if request.method == 'POST':
        sf = SignupForm(request.POST)

        valid_code = validate_signup(request.POST)
        if valid_code == 1:
            context['message'] = 'Passwords do not match'
        elif valid_code == 2:
            context['message'] = 'Username already taken!'
        elif valid_code == 3:
            context['message'] = 'Email already taken!'
        else:
            if sf.is_valid():
                new_user = User(
                    email_address=sf.cleaned_data.get('email_address'),
                    username=sf.cleaned_data.get('username'),
                    password=sf.cleaned_data.get('password')
                )
                new_user.save()
                context['message'] = 'Account created!'
                return redirect('/')

            context['message'] = 'Signup is invalid!'

        return render(request, 'login/signup.html', context)

    return render(request, 'login/signup.html')
