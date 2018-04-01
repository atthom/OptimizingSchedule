from django.shortcuts import render
from django.views.generic import TemplateView

def welcome(request):
    return render(request, 'welcome.html', context={})