from pipes import Template
from django.shortcuts import render
from django.contrib import messages
from . import models, forms

from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'dash/index.html'


