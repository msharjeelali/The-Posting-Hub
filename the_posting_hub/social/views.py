from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Post, Like, Comment, Draft, Bookmark
from .forms import PostForm, SearchForm, UserProfileForm, UserEditForm, CustomPasswordChangeForm, CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
# Create your views here.
# social/views.py

@require_POST
@login_required
def delete_account(request):
    user = request.user
    password = request.POST.get('password')
    
    if not user.check_password(password):
        messages.error(request, 'Incorrect password. Account not deleted.')
        return redirect('dashboard')
    
    try:
        logout(request)
        user.delete()
        messages.success(request, 'Your account has been permanently deleted.')
        return redirect('home')  # Redirect to your home page or another app
    except Exception as e:
        messages.error(request, f'Error deleting account: {str(e)}')
        return redirect('dashboard')

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
        if 'save_draft' in request.POST:
            if form.is_valid():
                draft = Draft(
                    title=form.cleaned_data['title'],
                    content=form.cleaned_data['content'],
                    author=request.user
                )
                draft.save()
                messages.success(request, 'Your draft has been saved!')
                return redirect('view_drafts_list')
        elif form.is_valid():
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
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')  # or your post detail view
    else:
        form = PostForm(instance=post)  # pre-fill the form
    return render(request, 'social/create_post.html', {
        'form': form,
        'post': post,  # optional, in case you want title/content in template
        'is_edit': True  # template can change button label etc.
    })


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

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        password_form = CustomPasswordChangeForm(user=request.user, data=request.POST if any(
            field in request.POST for field in ['old_password', 'new_password1', 'new_password2']
        ) else None)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            
            # Only validate password if any field was filled
            if any(field in request.POST for field in ['old_password', 'new_password1', 'new_password2']):
                if password_form.is_valid():
                    password_form.save()
                    update_session_auth_hash(request, password_form.user)
                    messages.success(request, 'Password updated successfully!')
                else:
                    # If password change was attempted but invalid, show errors
                    for field, errors in password_form.errors.items():
                        for error in errors:
                            messages.error(request, f"Password error: {error}")
                    return redirect('edit_profile')
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('edit_profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
        password_form = CustomPasswordChangeForm(user=request.user)
    
    return render(request, 'social/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form,
    })

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('dashboard')
    
    # If not POST, show confirmation (optional)
    return render(request, 'social/confirm_delete.html', {'post': post})

@login_required
def user_homepage(request):
    posts = Post.objects.exclude(author=request.user).order_by('-created_at')
    post_data = []
    for post in posts:
        likes_count = post.likes.filter(is_active=True).count()
        comments_count = post.comments.filter(is_active=True).count()
        user_liked = post.likes.filter(user=request.user, is_active=True).exists()
        user_bookmarked = Bookmark.objects.filter(user=request.user, post=post, is_active=True).exists()
        post_data.append({
            'post': post,
            'likes_count': likes_count,
            'comments_count': comments_count,
            'user_liked': user_liked,
            'user_bookmarked': user_bookmarked,
        })
    return render(request, 'social/user_homepage.html', {'post_data': post_data})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if like.is_active:
        like.is_active = False  # Unlike
    else:
        like.is_active = True   # Like
    like.save()
    return HttpResponseRedirect(reverse('user_homepage'))

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('user_homepage')
    else:
        form = CommentForm()
    return render(request, 'social/add_comment.html', {'form': form, 'post': post})

@login_required
def view_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    likes = post.likes.filter(is_active=True)
    comments = post.comments.filter(is_active=True).order_by('created_at')
    return render(request, 'social/view_post.html', {
        'post': post,
        'likes': likes,
        'comments': comments,
    })

@login_required
def view_drafts_list(request):
    drafts = Draft.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'social/view_drafts_list.html', {'drafts': drafts})

@login_required
def edit_draft(request, draft_id):
    draft = get_object_or_404(Draft, id=draft_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, initial={'title': draft.title, 'content': draft.content})
        if 'save_draft' in request.POST:
            if form.is_valid():
                draft.title = form.cleaned_data['title']
                draft.content = form.cleaned_data['content']
                draft.save()
                messages.success(request, 'Draft updated successfully!')
                return redirect('view_drafts_list')
        elif 'publish' in request.POST:
            if form.is_valid():
                post = Post(
                    title=form.cleaned_data['title'],
                    content=form.cleaned_data['content'],
                    author=request.user
                )
                post.save()
                draft.delete()
                messages.success(request, 'Draft published as a post!')
                return redirect('dashboard')
    else:
        form = PostForm(initial={'title': draft.title, 'content': draft.content})
    return render(request, 'social/edit_draft.html', {'form': form, 'draft': draft})

@login_required
def bookmark_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    bookmark, created = Bookmark.objects.get_or_create(post=post, user=request.user)
    if bookmark.is_active:
        bookmark.is_active = False  # Unbookmark
    else:
        bookmark.is_active = True   # Bookmark
    bookmark.save()
    return HttpResponseRedirect(reverse('user_homepage'))

@login_required
def view_saved_posts(request):
    bookmarks = Bookmark.objects.filter(user=request.user, is_active=True).select_related('post').order_by('-date_saved')
    posts = [bookmark.post for bookmark in bookmarks]
    return render(request, 'social/view_saved_posts.html', {'posts': posts})