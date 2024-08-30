from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib import messages
from .models import *
from .forms import *
from django.views.generic import CreateView, DetailView


class CategoryCreateView(CreateView, LoginRequiredMixin):
    
    model = TicketCategory
    form_class = TicketCategoryForm
    template_name = "core/category_create.html"
    login_url = "login"
    
    def form_valid(self, form):
        form.instance.createdBy = self.request.user
        form.instance.save(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("categories:category_detail", kwargs={"pk": self.object.pk})


class CategoryDetailView(DetailView):
    
    model = TicketCategory
    template_name = "core/category_detail.html"
    context_object_name = "category"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = TicketCategory.objects.get(pk=self.kwargs["pk"])
        
        return context