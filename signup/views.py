from django.shortcuts import render, redirect

from login.models import User

# Create your views here.
def signup_view(request):
    request.session['error_message'] = ''
    if request.method == 'POST':
        email = request.POST['email_field']
        username = request.POST['username_field']
        password = request.POST['password_field']
        confirm_password = request.POST['password_field_confirm']

        if confirm_password != password:
            request.session['error_message'] = 'passwords do not match'

        for i in User.objects.all():
            user = User.objects.get(id=i.pk)
            if username == user.username:
                request.session['error_message'] = 'username already taken'
                break
            elif email == user.email_address:
                request.session['error_message'] = 'email already in use'
                break
        
        if request.session['error_message'] == '':
            User.objects.create(email_address=email, username=username, password=password)
            request.session['error_message'] = 'account created!'
            return redirect('/')
    else:
        request.session['error_message'] = ''
    context = {
        'error_message': request.session['error_message'],
        'user_index': request.session['user_index'],
    }
    return render(request, "signup/signup.html", context)
