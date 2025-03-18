from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import Blog, Profile, Comment
from django.db import models
from django.contrib.auth import logout


# Create your views here.

def index(request):
    """view for render home page"""
    template_name = 'base.html'
    return render(request, template_name=template_name)


class BlogListView(ListView):
    model = Blog
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset_without_archived = queryset.filter(is_archived=False)
        return queryset_without_archived


class BlogDetailView(DetailView):
    queryset = Blog.objects.select_related('author__user').prefetch_related(
        models.Prefetch('comments', queryset=Comment.objects.filter(is_archived=False))
    ).all()


class BlogCreateView(LoginRequiredMixin,CreateView):
    model = Blog
    fields = 'title', 'content',

    def form_valid(self, form):
        user = self.request.user
        form.instance.author = Profile.objects.get(user=user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('microblog:blog-detail', kwargs={'pk':self.object.pk})


class BloggerListView(ListView):
    model = Profile

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('user').filter(is_blogger=True)
        return queryset


class BloggerDetailView(DetailView):
    queryset = Profile.objects.select_related('user').prefetch_related("blogs").all()


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = 'content',

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog'] = Blog.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        user = self.request.user
        form.instance.author = Profile.objects.get(user=user)
        form.instance.blog = Blog.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('microblog:blog-detail', kwargs={'pk':self.kwargs['pk']})

