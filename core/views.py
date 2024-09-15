from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Ticket, TicketCategory, TicketReport
from .forms import TicketForm, TicketCategoryForm, TicketReportForm


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


class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'core/ticket_list.html'
    context_object_name = 'ticket_list'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TicketForm()
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket = self.get_object()
        context['ticket'] = ticket
        context['form'] = TicketReportForm(initial={'ticket': ticket})
        context['reports'] = TicketReport.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = TicketReportForm(request.POST)
        if form.is_valid():
            ticket_report = form.save(commit=False)
            ticket_report.ticket = self.object
            ticket_report.save()
            return redirect(reverse_lazy('core:detail-ticket', kwargs={'pk': self.object.pk}))
        else:
            return self.render_to_response(self.get_context_data(form=form))
