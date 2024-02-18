from django.contrib import admin

# Register your models here.
from .models import Post, PostPoint, Comment

admin.site.register(Post)
admin.site.register(PostPoint)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', "name", "emeil", 'text', 'date_create', 'date_update', 'active')
    list_filter=("date_create",)
    search_fields = ("emeil", "post", "text", "active")
