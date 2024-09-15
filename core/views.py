from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.contrib import messages
from .models import *
from .forms import *
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView


class CategoryListView(ListView):
    model = TicketCategory
    template_name = "core/category_list.html"
    context_object_name = "category_list"
    login_url = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TicketCategoryForm()
        return context


class CategoryCreateView(CreateView):   
    model = TicketCategory
    form_class = TicketCategoryForm
    template_name = "core/category_create.html"
    login_url = "login"
    success_url = reverse_lazy("core:categories")

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
        context["category"] = TicketCategory.objects.get(pk=self.kwargs["pk"])
        return context


class TicketListView(ListView):
    model = Ticket
    template_name = "core/ticket_list.html"
    context_object_name = "ticket_list"
    login_url = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TicketForm()
        context["categories"] = TicketCategory.objects.all()
        return context


class TicketCreateView(CreateView):
    model = Ticket
    template_name = "core/ticket_create.html"
    form_class = TicketForm
    success_url = reverse_lazy("core:tickets")

    def form_valid(self, form):
        form.instance.createdBy = self.request.user
        form.instance.save()
        return super().form_valid(form)


class TicketDetailView(DeleteView):
    model = Ticket
    template_name = "core/ticket_detail.html"
    context_object_name = "ticket"
    login_url = "login"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket = Ticket.objects.get(pk=self.kwargs["pk"])
        context["ticket"] = ticket
        return context