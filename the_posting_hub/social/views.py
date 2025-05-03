from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Post
from .forms import PostForm, SearchForm
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

@login_required
def search(request):
    form = SearchForm(request.GET)
    results = {'users': [], 'posts': []}
    
    if form.is_valid():
        query = form.cleaned_data['query']
        
        # Search for users
        users = User.objects.filter(
            username__icontains=query
        ) | User.objects.filter(
            first_name__icontains=query
        ) | User.objects.filter(
            last_name__icontains=query
        )
        results['users'] = users
        
        # Search for posts
        posts = Post.objects.filter(
            title__icontains=query
        ) | Post.objects.filter(
            content__icontains=query
        )
        results['posts'] = posts
    
    context = {
        'form': form,
        'results': results,
        'query': request.GET.get('query', ''),
        'page_title': 'Search Results'
    }
    return render(request, 'social/search.html', context)

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('/')
