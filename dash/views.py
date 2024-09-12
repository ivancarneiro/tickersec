from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'dash/index.html'
    login_url = 'login'