from django.shortcuts import render

# Create your views here.
from django.views.generic.list import ListView
from studentorg.models import Organization

class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    template_name = "home.html" 