from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Profile, Blog,Comment

# Register your models here.
@admin.action(description='Archive')
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(is_archived=True)


@admin.action(description='Unarchive')
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(is_archived=False)


@admin.register(Profile)
class BloggerModelAdmin(admin.ModelAdmin):
    list_display = 'user', 'bio', 'is_blogger'


@admin.register(Blog)
class BlogModelAdmin(admin.ModelAdmin):
    actions = [mark_unarchived, mark_archived]
    list_display = 'title', 'author', 'created_at', 'content', 'is_archived'

    def short_content(self, obj: Blog):
        if len(obj.content) > 50:
            return obj.content[:50] + '...'
        return obj.content


@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    actions = [mark_unarchived, mark_archived]
    list_display = 'blog', 'author', 'short_content', 'created_at', 'is_archived'

    def short_content(self, obj: Comment) -> str:
        if len(obj.content) > 50:
            return obj.content[:50] + '...'
        return obj.content
