from os import name
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import IndexView
from .forms import LoginForm


app_name = 'dash'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]
