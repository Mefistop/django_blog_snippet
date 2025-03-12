from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from .models import Blog, Profile, Comment


# Create your views here.

def index(request):
    """view for render home page"""
    template_name = 'base.html'
    return render(request, template_name=template_name)


class BlogListView(ListView):
    model = Blog

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_archived=False)
        return queryset


class BloggerListView(ListView):
    model = Profile

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_blogger=True)
        return queryset