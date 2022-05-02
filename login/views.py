from ctypes.wintypes import HRSRC
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages, auth

from .models import Account, UserAccount
from .forms import LoginForm, SignupForm, EditAccountForm, EditUsername, EditPassword

def account_view(request):
    if request.user.id is not None:
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
    else:
        message = ''
    form = LoginForm()
    
    context= {'message': message, 'form': form}
    return render(request, 'login/login.html', context)

def logout_view(request):
    if request.method == 'POST':
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
    if request.user.id is not None:
        account = Account.objects.get(id=request.user.id)
        user = UserAccount.objects.get(user_id=request.user.id)
        if request.method == 'POST':
            form = EditUsername(request.POST, instance=user)
            password_form = EditPassword(request.POST, instance=user)
            if form.is_valid():
                account.username = form.cleaned_data['username']
                account.save()
                return redirect('/account')
            else:
                return redirect('edit_account')
        else:
            form = EditUsername(request.GET, instance=user)
            password_form = EditPassword(request.GET, instance=user)
            form.fields['username'].widget.attrs = {'value': account.username, 'class': 'account_field'}
            password_form.fields['password'].widget.attrs = {'placeholder': 'password', 'class': 'account_field'}
            password_form.fields['confirm_password'].widget.attrs = {'placeholder': 'confirm password', 'class': 'account_field'}
            context = {'user': user, 'form': form, 'account': account, 'password_form': password_form}
            return render(request, 'login/edit_account.html', context)
    else:
        return redirect('login')

def edit_password_view(request):
    print('edit password')
    account = Account.objects.get(id=request.user.id)
    user = UserAccount.objects.get(user_id=request.user.id)
    form = EditPassword(request.POST, instance=user)
    if form.cleaned_data['password'] != form.cleaned_data['confirm_password']:
        message = 'Passwords do not match'
        return redirect('account')
    elif form.is_valid():
        password = form.cleaned_data['password']
        account.set_password(password)
        account.save()
        return redirect('account')
    else:
        message = 'Username or Email already taken!'
    return redirect('edit_account')