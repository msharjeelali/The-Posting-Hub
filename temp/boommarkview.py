# views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Post, Bookmark

@login_required
def toggle_bookmark(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, post=post)

    if not created:
        bookmark.delete()
        messages.info(request, f"Removed bookmark from: {post.title}")
    else:
        messages.success(request, f"Bookmarked: {post.title}")

    return redirect('post_detail', post_id=post.id)
