"""
URL configuration for snippet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from .views import (
    BlogCreateView,
    BlogDeleteView,
    BlogDetailView,
    BloggerDetailView,
    BloggerListView,
    BlogListView,
    BlogUpdateView,
    CommentCreateView,
    index,
)

app_name = "microblog"

urlpatterns = [
    path("", index, name="index"),
    path("blogs/", BlogListView.as_view(), name="blog-list"),
    path("blogs/<int:pk>", BlogDetailView.as_view(), name="blog-detail"),
    path("blogs/create", BlogCreateView.as_view(), name="blog-create"),
    path("blogs/<int:pk>/update", BlogUpdateView.as_view(), name="blog-update"),
    path("blogs/<int:pk>/delete", BlogDeleteView.as_view(), name="blog-delete"),
    path("bloggers/", BloggerListView.as_view(), name="blogger-list"),
    path("bloggers/<int:pk>", BloggerDetailView.as_view(), name="blogger-detail"),
    path(
        "blogs/<int:pk>/create_comment",
        CommentCreateView.as_view(),
        name="comment-create",
    ),
]
