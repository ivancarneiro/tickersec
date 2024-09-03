from msilib.schema import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.contrib import messages
from .models import *
from .forms import *
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView


class CategoryCreateView(LoginRequiredMixin, CreateView):
    
    model = TicketCategory
    form_class = TicketCategoryForm
    template_name = "core/category_create.html"
    login_url = "login"
    success_url = reverse_lazy("core/category_list.html")
    
    def form_valid(self, form):
        form.instance.createdBy = self.request.user
        form.instance.save(form)
        return super().form_valid(form)


class CategoryDetailView(DetailView):
    
    model = TicketCategory
    template_name = "core/category_detail.html"
    context_object_name = "category"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = TicketCategory.objects.get(pk=self.kwargs["pk"])
        return context


class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = "core/ticket_list.html"
    context_object_name = "ticket_list"
    login_url = "login"


