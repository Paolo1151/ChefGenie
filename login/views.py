from django.shortcuts import redirect, render
from django.http import HttpResponse

from .models import User
from .forms import LoginForm

#variables
user_index = 0
error_message = ''

def change_user_index(number):
    user_index = number

# Create your views here
def account_view(request):
    if user_index != 0:
        user = User.objects.get(id=user_index)
        context = {
            'user_index': user_index,
            'current_user': user
        }
    else:
        context = {
            'user_index': user_index
        }
    return render(request, "account/account.html", context)

def login_view(request):
    global error_message
    if request.method == 'POST':
        username = request.POST['username_field']
        password = request.POST['password_field']
        error_message = ''

        for i in User.objects.all():
            user = User.objects.get(id=i.pk)
            if user.username == username and user.password == password:
                global user_index 
                user_index = i.pk
                return redirect('account')
        error_message = 'invalid username or password'
    context = {
        'error_message': error_message,
        'user_index': user_index,
    }
    return render(request, "login/login.html", context)

