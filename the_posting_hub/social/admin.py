from django.contrib import admin
from .models import Post, Comment, Like

# Register your models here.
admin.site.register(Comment)
admin.site.register(Like)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    list_filter = ('created_at', 'author')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at'
