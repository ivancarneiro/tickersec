from typing import Any
from django.views.generic import TemplateView
from .graficos import barTicketSeveritiesXmonth, pieTicketSeverities, pieTicketCategories


class IndexView(TemplateView):
    template_name = 'dash/index.html'
    login_url = 'login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['ticketSevBar'] = barTicketSeveritiesXmonth()
        context['ticketSevPie'] = pieTicketSeverities()
        context['ticketCatPie'] = pieTicketCategories()
    
        return context