from django.contrib import admin
from .models import Post, Comment, Like, ReportUser, ReportPost, ReportComment

# Register your models here.
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(ReportUser)
admin.site.register(ReportPost)
admin.site.register(ReportComment)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    list_filter = ('created_at', 'author')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at'
