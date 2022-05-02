from ctypes.wintypes import HRSRC
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages, auth

from .models import Account, UserAccount
from .forms import LoginForm, SignupForm, EditAccountForm

from recipe.utils.search.engine import SearchEngine

def account_view(request):
    if request.user.id:
        account = Account.objects.get(id=request.user.id)
        user = UserAccount.objects.get(user_id=request.user.id)
        context = {'account': account, 'user': user}
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
        account = Account.objects.get(id=request.user.id)
        user = UserAccount.objects.get(user_id=request.user.id)
        weightGoalMet = user.weight == user.weight_goal
        weightBelowGoal = user.weight < user.weight_goal
        weightDifference = abs(user.weight_goal - user.weight)
        calories_consumed = user.calorie_goal - SearchEngine.calculate_calorie_goal(user)
        context = {
            'account': account, 'user': user, 'weightGoalMet': weightGoalMet,
            'weightBelowGoal': weightBelowGoal, 'weightDifference': weightDifference,
            'calories_consumed': calories_consumed
        }
        return render(request, 'home/home.html', context)
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
        user = UserAccount.objects.get(user_id=request.user.id)
        if request.method == 'POST':
            form = EditAccountForm(request.POST, instance=user)
            form.save()
            return redirect('/account')
        else:
            form = EditAccountForm()
            context = {'user': user, 'form': form}
            return render(request, 'login/edit_account.html', context)
    else:
        return redirect('login')
