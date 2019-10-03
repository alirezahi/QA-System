from django.shortcuts import render
from django.views.generic import TemplateView
from language_skills.utilities import a

# Create your views here.


class TestView(TemplateView):
    template_name = 'test.html'
    
    def get_context_data(self, **kwargs):
        context = super(TestView, self).get_context_data(**kwargs)
        context['sample'] = a.tojson()
        return context