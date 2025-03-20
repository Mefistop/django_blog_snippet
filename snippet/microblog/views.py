from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Blog, Comment, Profile

# Create your views here.


def index(request):
    """view for render home page"""

    template_name = "base.html"
    return render(request, template_name=template_name)


class BlogListView(ListView):
    model = Blog
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset_without_archived = queryset.filter(is_archived=False)
        return queryset_without_archived


class BlogDetailView(DetailView):
    queryset = (
        Blog.objects.select_related("author__user")
        .prefetch_related(
            models.Prefetch(
                "comments", queryset=Comment.objects.filter(is_archived=False)
            )
        )
        .all()
    )


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ("title", "content")

    def form_valid(self, form):
        user = self.request.user
        form.instance.author = Profile.objects.get(user=user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("microblog:blog-detail", kwargs={"pk": self.object.pk})


class BlogUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):

    def test_func(self):
        blog = self.get_object()
        return self.request.user == blog.author.user

    model = Blog
    fields = ("title", "content")
    template_name = "microblog/blog_update_form.html"

    def form_valid(self, form):
        user = self.request.user
        form.instance.author = Profile.objects.get(user=user)
        return super().form_valid(form)


class BlogDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):

    def test_func(self):
        blog = self.get_object()
        return self.request.user == blog.author.user

    model = Blog
    success_url = reverse_lazy("microblog:blog-list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.is_archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class BloggerListView(ListView):
    model = Profile

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("user").filter(is_blogger=True)
        return queryset


class BloggerDetailView(DetailView):
    queryset = Profile.objects.select_related("user").prefetch_related("blogs").all()


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ("content",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blog"] = Blog.objects.get(pk=self.kwargs["pk"])
        return context

    def form_valid(self, form):
        user = self.request.user
        form.instance.author = Profile.objects.get(user=user)
        form.instance.blog = Blog.objects.get(pk=self.kwargs["pk"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("microblog:blog-detail", kwargs={"pk": self.kwargs["pk"]})
