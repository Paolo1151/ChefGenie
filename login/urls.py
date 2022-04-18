from django.urls import path

from .views import login_view, logout_view, account_view, signup_view

urlpatterns = [
    path('', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('signup', signup_view, name='signup'),
    path('account', account_view, name='account'),
]