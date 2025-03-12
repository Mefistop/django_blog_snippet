from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class Profile(models.Model):
    """Blogger model"""
    bio = models.TextField(blank=True)
    is_blogger = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        if self.is_blogger:
            return f"Blogger {self.user.username}"
        return f"User {self.user.username}"

    def get_absolute_url(self):
        pass


class Blog(models.Model):
    """Blog model, add validation: bloggers with 'is blogger' = True can post blog"""
    class Meta:
        ordering = ['-created_at']

    title = models.CharField(null=False, max_length=200, blank=False)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_archived = models.BooleanField(default=False)

    def clean(self):
        if not self.author.is_blogger:
            raise ValidationError("Only bloggers can create a blog.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Blog "{self.title}" by {self.author.user.username}'

    def get_absolute_url(self):
        pass


class Comment(models.Model):
    """Comment model"""
    class Meta:
        ordering = ['-created_at']

    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    content = models.CharField(null=False, max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment to blog with title '{self.blog.title}' by {self.author.user.username}"

