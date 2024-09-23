from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import *
from .forms import *


class CategoryListView(LoginRequiredMixin, ListView):
    model = TicketCategory
    template_name = 'core/category_list.html'
    context_object_name = 'category_list'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TicketCategoryForm()
        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = TicketCategory
    form_class = TicketCategoryForm
    template_name = 'core/category_create.html'
    login_url = 'login'
    success_url = reverse_lazy('core:categories')

    def form_valid(self, form):
        form.instance.createdBy = self.request.user
        return super().form_valid(form)


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = TicketCategory
    template_name = 'core/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_object()
        return context


class TicketListView(ListView):
    model = Ticket
    template_name = 'core/ticket_list.html'
    context_object_name = 'ticket_list'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['newTicketForm'] = TicketForm()
        context['categories'] = TicketCategory.objects.all()
        return context


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    template_name = 'core/ticket_create.html'
    form_class = TicketForm
    success_url = reverse_lazy('core:tickets')

    def form_valid(self, form):
        form.instance.createdBy = self.request.user
        return super().form_valid(form)


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = 'core/ticket_detail.html'
    context_object_name = 'ticket'
    login_url = 'login'
    form_class = TicketReportForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket = self.get_object()
        context['ticket'] = ticket
        context['form'] = TicketReportForm(initial={'ticket': ticket})
        context['reports'] = ticket.reportes.all()
        return context

    def form_valid(self, form):
        form.instance.createdBy = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = TicketReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.ticket = self.get_object()
            report.createdBy = self.request.user
            report.save()
            self.get_object().update_ticketStatus()
            return redirect(reverse_lazy('core:detail-ticket', kwargs={'pk': report.ticket.pk}))
        else:
            return self.render_to_response(self.get_context_data(form=form))


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    template_name = 'core/ticket_update.html'
    form_class = TicketUpdateForm
    login_url = 'login'

    def get_success_url(self):
        return reverse_lazy('core:detail-ticket', kwargs={'pk': self.get_object().pk})
