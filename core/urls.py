from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
from .forms import *


app_name = 'core'

urlpatterns = [
    path("tickets/", TicketListView.as_view(), name="tickets"),
]