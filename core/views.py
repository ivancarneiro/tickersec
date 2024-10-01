from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
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
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        form = TicketSearchForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['q']:
                queryset = queryset.filter(title__icontains=form.cleaned_data['q'])
            if form.cleaned_data['type']:
                queryset = queryset.filter(type=form.cleaned_data['type'])
            if form.cleaned_data['category']:
                queryset = queryset.filter(category=form.cleaned_data['category'])
            if form.cleaned_data['severity']:
                queryset = queryset.filter(severity=form.cleaned_data['severity'])
            if form.cleaned_data['impact']:
                queryset = queryset.filter(impact=form.cleaned_data['impact'])
            if form.cleaned_data['assignedTo']:
                queryset = queryset.filter(assignedTo=form.cleaned_data['assignedTo'])
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['newTicketForm'] = TicketForm()
        context['categories'] = TicketCategory.objects.all()
        context['searchForm'] = TicketSearchForm(self.request.GET)
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
        context['reportForm'] = TicketReportForm(initial={'ticket': ticket})
        context['reports'] = ticket.reportes.all()
        return context

    def post(self, request, *args, **kwargs):
        form = TicketReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.ticket = self.get_object()
            report.createdBy = self.request.user
            report.save()
            action = form.cleaned_data.get('action')
            self.get_object().update_ticketStatus(action=action)
            messages.success(request, 'Reporte creado y estado del ticket actualizado.')
            return redirect(reverse_lazy('core:detail-ticket', kwargs={'pk': report.ticket.pk}))
        else:
            messages.error(request, 'Hubo un error al crear el reporte.')
            return self.render_to_response(self.get_context_data(form=form))


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    template_name = 'core/ticket_update.html'
    form_class = TicketUpdateForm
    login_url = 'login'

    def get_success_url(self):
        return reverse_lazy('core:detail-ticket', kwargs={'pk': self.get_object().pk})

# TODO falta manejar el request para el valor de action, que debería modificar el estado de un ticket en caso de elegir Cerrar.