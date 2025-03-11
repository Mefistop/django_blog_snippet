from django.shortcuts import render
from django.views import View

# Create your views here.

def index(request):
    template_name = 'microblog/base.html'
    return render(request, template_name=template_name)
