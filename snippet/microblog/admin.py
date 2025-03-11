from django.contrib import admin
from .models import BloggerModel, BlogModel,CommentModel

# Register your models here.

@admin.register(BloggerModel)
class BloggerModelAdmin(admin.ModelAdmin):
    list_display = 'user', 'bio', 'is_blogger'


@admin.register(BlogModel)
class BlogModelAdmin(admin.ModelAdmin):
    list_display = 'title', 'author', 'created_at', 'content', 'is_archived'


@admin.register(CommentModel)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = 'blog', 'author', 'short_content', 'created_at', 'is_archived'

    def short_content(self, obj: CommentModel) -> str:
        if len(obj.content) > 50:
            return obj.content[:50] + '...'
        return obj.content
