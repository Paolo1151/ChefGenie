from django.shortcuts import redirect, render
from django.http import HttpResponse

from .models import User
from .forms import LoginForm

#variables

# Create your views here
def account_view(request):
    if request.session['user_index'] != 0:
        user = User.objects.get(id=request.session['user_index'])
        context = {
            'user_index': request.session['user_index'],
            'current_user': user
        }
    else:
        context = {
            'user_index': request.session['user_index']
        }
    return render(request, "account/account.html", context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username_field']
        password = request.POST['password_field']

        for i in User.objects.all():
            user = User.objects.get(id=i.pk)
            if user.username == username and user.password == password:
                request.session['user_index'] = i.pk
                return redirect('account')
        request.session['error_message'] = 'invalid username or password'
    #else:
        #request.session['error_message'] = ''
    context = {
        'error_message': request.session['error_message'],
        'user_index': request.session['user_index'],
    }
    return render(request, "login/login.html", context)

