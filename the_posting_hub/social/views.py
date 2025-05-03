from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Post
from .forms import PostForm, SearchForm, UserProfileForm, UserEditForm, CustomPasswordChangeForm
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

# @login_required
# def edit_profile(request):
#     # ---------------------------------------
#     # if request.method == 'POST':
#     #     form = UserProfileForm(request.POST, instance=request.user.profile)
#     #     if form.is_valid():
#     #         form.save()
#     #         messages.success(request, 'Your profile was successfully updated!')
#     #         return redirect('dashboard')
#     #     else:
#     #         messages.error(request, 'Please correct the errors below.')
#     # else:
#     #     form = UserProfileForm(instance=request.user.profile)
#     # context = {
#     #     'form': form,
#     #     'page_title': 'Edit Profile'
#     # }
#     # return render(request, 'social/edit_profile.html', context)
#     # ---------------------------------------
#     if request.method == 'POST':
#         user_form = UserEditForm(request.POST, instance=request.user)
#         profile_form = UserProfileForm(request.POST, instance=request.user.profile)
#         password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        
#         if 'user_info' in request.POST and user_form.is_valid():
#             user_form.save()
#             messages.success(request, 'Your profile information was updated!')
#             return redirect('edit_profile')
            
#         if 'profile_info' in request.POST and profile_form.is_valid():
#             profile_form.save()
#             messages.success(request, 'Your profile details were updated!')
#             return redirect('edit_profile')
            
#         if 'change_password' in request.POST and password_form.is_valid():
#             password_form.save()
#             update_session_auth_hash(request, password_form.user)
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect('edit_profile')
#     else:
#         user_form = UserEditForm(instance=request.user)
#         profile_form = UserProfileForm(instance=request.user.profile)
#         password_form = CustomPasswordChangeForm(user=request.user)
    
#     return render(request, 'social/edit_profile.html', {
#         'user_form': user_form,
#         'profile_form': profile_form,
#         'password_form': password_form,
#     })
# views.py
@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.profile)
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