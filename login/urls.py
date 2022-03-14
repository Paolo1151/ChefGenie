from django.urls import path

from .views import login_view, account_view

urlpatterns = [
    path('', login_view, name='login'),
    path('account', account_view, name='account'),
]