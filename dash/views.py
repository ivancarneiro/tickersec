from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'dash/index.html'
    login_url = 'login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['ticketSevBar'] = {}
    
        return context