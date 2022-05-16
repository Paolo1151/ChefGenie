from ctypes.wintypes import HRSRC
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages, auth
from django.contrib.auth import update_session_auth_hash

from .models import Account, UserAccount
from .forms import LoginForm, SignupForm, EditAccountForm, EditUsername, EditPassword

message = ''

from recipe.utils.search.engine import SearchEngine

def account_view(request):
    if request.user.id:
        account = Account.objects.get(id=request.user.id)
        user = UserAccount.objects.get(user_id=request.user.id)
        if request.method == 'POST':
            form = EditAccountForm(request.POST, request.FILES, instance=user)
            form.save()
            return redirect('/account')
        else:
            form = EditAccountForm(request.GET, instance=user)
            form.fields['weight'].widget.attrs = {'value': user.weight, 'class': 'account_field'}
            form.fields['height'].widget.attrs = {'value': user.height, 'class': 'account_field'}
            form.fields['weight_goal'].widget.attrs = {'value': user.weight_goal, 'class': 'account_field'}
            form.fields['calorie_goal'].widget.attrs = {'value': user.calorie_goal, 'class': 'account_field'}
            context = {'user': user, 'form': form, 'account': account}
            return render(request, 'login/account.html', context)
    else:
        return redirect('login')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(request=request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('account')
        else:
            message = 'invalid username or password'
    elif request.user.id:
        return redirect('/home/new')
    else:
        message = ''
    form = LoginForm()
    
    context= {'message': message, 'form': form}
    return render(request, 'login/login.html', context)


def logout_view(request):
    auth.logout(request)
    return redirect('login')


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email_address = form.cleaned_data['email_address']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = Account.objects.create_user(email_address=email_address, username=username)
            user.set_password(password)
            user.save()
            user_account = UserAccount()
            user_account.user_id = user.id
            user_account.save()
            message = 'Account created!'
            return redirect('/')
        elif(form.cleaned_data['password'] != form.cleaned_data['confirm_password']):
                message = 'Passwords do not match'
        else:
            message = 'Username or Email already taken!'
    else:
        message = ''
        form = SignupForm()

    context = {'message': message, 'form': form}
    return render(request, 'login/signup.html', context)


def edit_account_view(request):
    username_message = None
    password_message = None
    if request.user.id is not None:
        account = Account.objects.get(id=request.user.id)
        user = UserAccount.objects.get(user_id=request.user.id)
        form = EditUsername(request.GET, instance=user)
        password_form = EditPassword(request.GET, instance=account)
        form.fields['username'].widget.attrs = {'value': account.username, 'class': 'account_field'}
        password_form.fields['password'].widget.attrs = {'placeholder': 'Password', 'class': 'account_field'}
        password_form.fields['confirm_password'].widget.attrs = {'placeholder': 'Confirm Password', 'class': 'account_field'}
        if request.method == 'POST':
            form = EditUsername(request.POST, instance=user)
            password_form = EditPassword(request.POST, instance=account)
            if form.is_valid():
                if Account.objects.filter(username=form.cleaned_data['username']).exists():
                    username_message = 'username taken'
                    context = {'user': user, 'form': form, 'account': account, 'password_form': password_form, 'username_message': username_message}
                    return render(request, 'login/edit_account.html', context)
                else:
                    account.username = form.cleaned_data['username']
                    account.save()
                    return redirect('/account')
            else:
                return redirect('edit_account')
        else:
            context = {'user': user, 'form': form, 'account': account, 'password_form': password_form, 'username_message': username_message}
            return render(request, 'login/edit_account.html', context)
    else:
        return redirect('login')


def edit_password_view(request):
    account = Account.objects.get(id=request.user.id)
    password_form = EditPassword(request.POST, instance=account)
    if password_form.is_valid():
        if (password_form.cleaned_data['password'] != password_form.cleaned_data['confirm_password']):
            message = 'Passwords do not match'
            return redirect('account')
        elif password_form.is_valid():
            password = password_form.cleaned_data['password']
            account.set_password(password)
            account.save()
            update_session_auth_hash(request, account)
            return redirect('edit_account')
        else:
            message = 'Username or Email already taken!'
    return redirect('edit_account')