from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post
from .forms import PostForm
# Create your views here.
# social/views.py

@login_required
def dashboard(request):
    """
    This is the main feed/dashboard where users can see blog posts.
    In the future, this will display posts from the user and others they follow.
    """
    # Get the user's posts
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    
    context = {
        'posts': user_posts,
        'page_title': 'Your Feed'
    }
    return render(request, 'social/dashboard.html', context)

@login_required
def create_post(request):
    """
    View for creating a new blog post.
    """
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Your post has been created successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PostForm()
    
    return render(request, 'social/create_post.html', {'form': form, 'page_title': 'Create New Post'})
