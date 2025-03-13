from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from .models import Blog, Profile, Comment
from django.db import models


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


class BlogDetailView(DetailView):
    model = Blog
    queryset = Blog.objects.select_related('author__user').prefetch_related(
        models.Prefetch('comments', queryset=Comment.objects.filter(is_archived=False))
    ).all()


class BloggerListView(ListView):
    model = Profile

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('user').filter(is_blogger=True)
        return queryset


class BloggerDetailView(DetailView):
    model = Profile
    queryset = Profile.objects.select_related('user').prefetch_related("blogs").all()


class CommentCreateView(CreateView):
    model = Comment