from django.db import models
from django.db.models import CASCADE
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class BloggerModel(models.Model):
    """Blogger model"""
    bio = models.TextField(blank=True)
    is_blogger = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        if self.is_blogger:
            return f"Blogger {self.user.username}"
        return f"User {self.user.username}"


class BlogModel(models.Model):
    """Blog model"""
    title = models.CharField(null=False, max_length=200)
    author = models.ForeignKey(BloggerModel, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return f'Blog "{self.title}" by {self.author.user.username}'


class CommentModel(models.Model):
    """Comment model"""
    author = models.ForeignKey(BloggerModel, on_delete=models.CASCADE)
    blog = models.ForeignKey(BlogModel, on_delete=models.CASCADE)
    content = models.CharField(null=False, max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_archived = models.BooleanField(default=False)

