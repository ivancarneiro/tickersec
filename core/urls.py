from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
from .forms import *


app_name = 'core'

urlpatterns = [
    path("tickets/", TicketListView.as_view(), name="tickets"),
    path("tickets/new_ticket", TicketCreateView.as_view(), name="new_ticket"),
    path("categories/", CategoryListView.as_view(), name="categories"),
]