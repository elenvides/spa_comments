from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'created_at', 'parent_comment')
    readonly_fields = ["id", "user", "parent_comment", "created_at"]
    search_fields = ["user", "text"]
    ordering = ["-id"]
