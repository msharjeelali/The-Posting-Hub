from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Post, Like, Comment, Draft, Bookmark, Follow, ReportUser, ReportPost, ReportComment, Notification
from .forms import PostForm, SearchForm, UserProfileForm, UserEditForm, CustomPasswordChangeForm, CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.conf import settings



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
        if post.author != request.user:
            Notification.objects.create(
                to_user=post.author,
                from_user=request.user,
                notification_type='like',
                post=post
            )
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

            # Create notification for post author (if not commenting on own post)
            if post.author != request.user:
                Notification.objects.create(
                    to_user=post.author,
                    from_user=request.user,
                    notification_type='comment',
                    post=post,
                    comment=comment
                )

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
        'user': request.user,
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

@login_required
def view_profile(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(author=profile_user)
    
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()

    context = {
        'profile_user': profile_user,
        'posts': posts,
        'is_following': is_following,
    }
    return render(request, 'social/view_profile.html', context)

@login_required
def toggle_follow(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    current_user = request.user

    if target_user == current_user:
        messages.error(request, "You cannot follow yourself.")
        return redirect('view_profile', user_id=current_user.id)  # Fix for self-follow case

    existing_follow = Follow.objects.filter(follower=current_user, following=target_user).first()
    reverse_follow = Follow.objects.filter(follower=target_user, following=current_user).first()

    if existing_follow:
        # Unfollow and remove mutual follow if exists
        existing_follow.delete()
        if reverse_follow:
            reverse_follow.delete()
        messages.success(request, f"You unfollowed {target_user.username}.")
    else:
        # Follow user and ensure it's not mutual
        Follow.objects.create(follower=current_user, following=target_user)
        if reverse_follow:
            reverse_follow.delete()  # Remove reverse follow to ensure one-direction
        Notification.objects.create(
            to_user=target_user,
            from_user=current_user,
            notification_type='follow',
        )
        messages.success(request, f"You followed {target_user.username}.")

    # Redirect back to the target user's profile after both follow and unfollow actions
    return redirect('view_profile', user_id=target_user.id)  # Use user_id here

@login_required
def report_user(request, user_id):
    reported_user = get_object_or_404(User, id=user_id)
    reporter = request.user

    if reported_user == reporter:
        messages.error(request, "You cannot report yourself.")
        return redirect('view_profile', user_id=reporter.id)

    if request.method == "POST":
        reason = request.POST.get("reason")
        additional_info = request.POST.get("additional_info")

        ReportUser.objects.create(
            reporter=reporter,
            reported_user=reported_user,
            reason=reason,
            additional_info=additional_info
        )

        messages.success(request, "User report submitted successfully.")
        return redirect('view_profile', user_id=reported_user.id)

    return redirect('view_profile', user_id=reported_user.id)

@login_required
def report_post(request, post_id):
    post_to_report = get_object_or_404(Post, id=post_id)
    reporter = request.user

    if post_to_report.author == reporter:
        messages.error(request, "You cannot report your own post.")
        return redirect('view_post', post_id=post_to_report.id)

    if request.method == "POST":
        reason = request.POST.get('reason', 'Not specified')  # Fallback to default
        additional_info = request.POST.get('additional_info', '')

        try:
            report = ReportPost.objects.create(
                reporter=reporter,
                post=post_to_report,
                post_author=post_to_report.author,
                reason=reason,
                additional_info=additional_info
            )

            # Send email notification to admins
            subject = f"Post Report: {post_to_report.id}"
            message = f"{reporter.username} has reported Post ID {post_to_report.id} for {reason}."
            from_email = settings.DEFAULT_FROM_EMAIL
            admin_email = settings.ADMIN_EMAIL if hasattr(settings, 'ADMIN_EMAIL') else from_email

            send_mail(subject, message, from_email, [admin_email])
            messages.success(request, "Your report has been submitted to the admin.")
            
        except Exception as e:
            messages.error(request, f"Failed to submit report: {str(e)}")

        return redirect('view_post', post_id=post_to_report.id)

    return redirect('view_post', post_id=post_to_report.id)

@login_required
@require_POST
def report_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if comment.user == request.user:
        messages.error(request, "You cannot report your own comment.")
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    
    reason = request.POST.get('reason', '').strip()
    additional_info = request.POST.get('additional_info', '').strip()
    
    if not reason:
        messages.error(request, "Please select a reason for reporting.")
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    
    # Check if user has already reported this comment
    existing_report = ReportComment.objects.filter(
        comment=comment,
        reporter=request.user
    ).exists()
    
    if existing_report:
        messages.warning(request, "You have already reported this comment.")
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    
    try:
        report = ReportComment.objects.create(
            comment=comment,
            reporter=request.user,
            reason=reason,
            additional_info=additional_info if additional_info else None
        )

        # Send email notification to admins
        subject = f"Comment Report: {comment.id}"
        message = f"{request.user.username} has reported Comment ID {comment.id} on Post '{comment.post.title}' for {reason}."
        from_email = settings.DEFAULT_FROM_EMAIL
        admin_email = settings.ADMIN_EMAIL if hasattr(settings, 'ADMIN_EMAIL') else from_email

        send_mail(subject, message, from_email, [admin_email])
        messages.success(request, "Thank you for reporting this comment. Our team will review it.")
        
    except Exception as e:
        messages.error(request, f"Failed to submit report: {str(e)}")
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def view_notifications(request):
    notifications = Notification.objects.filter(to_user=request.user).order_by('-timestamp')
    return render(request, 'social/notification.html', {'notifications': notifications})

@login_required
def clear_all_notifications(request):
    if request.method == 'POST':
        # Delete all notifications for the current user (or mark them as read)
        deleted_count, _ = Notification.objects.filter(to_user=request.user).delete()
        # If you want to mark them as read instead, use the following line:
        # Notification.objects.filter(to_user=request.user).update(is_read=True)
        
        messages.success(request, f"Cleared {deleted_count} notifications.")
    else:
        messages.error(request, "Invalid request method")
    
    return redirect('notifications')  # Assuming you have a notifications URL name
