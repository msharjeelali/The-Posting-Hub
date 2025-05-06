from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor.fields import RichTextField

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"

class Draft(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='drafts')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Draft: {self.title} by {self.author.username}"

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='bookmarked_by')
    date_saved = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    notes = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ('user', 'post')
        ordering = ['-date_saved']

    def __str__(self):
        return f"{self.user.username} bookmarked {self.post.title}"

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower} follows {self.following}"

class ReportUser(models.Model):
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_received', null=True)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reports_made')
    reason = models.CharField(max_length=255, null=False, blank=False, default="Not specified")
    additional_info = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Report on user {self.reported_user.username} by {self.reporter.username}"

class ReportPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_reports_made')
    post_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_posts', null=True)
    reason = models.CharField(max_length=255, null=False, blank=False, default="Not specified")
    additional_info = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.post_author_id:
            self.post_author = self.post.author
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Report on post '{self.post.title}' by {self.reporter.username}"

class ReportComment(models.Model):
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_reports_made')
    
    # Track both the comment author and post author
    comment_author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='reported_comments',
        null=True  # In case user gets deleted
    )
    post_author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reported_comments_on_posts',
        null=True  # In case user gets deleted
    )
    
    reason = models.CharField(max_length=255, null=False, blank=False)
    additional_info = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    is_resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Comment Report'
        verbose_name_plural = 'Comment Reports'

    def save(self, *args, **kwargs):
        # Automatically set comment_author and post_author before saving
        if not self.comment_author_id:
            self.comment_author = self.comment.user
        if not self.post_author_id:
            self.post_author = self.comment.post.author
        super().save(*args, **kwargs)

    def __str__(self):
        return (f"Report on comment by {self.comment_author.username} "
                f"(Post by {self.post_author.username}) - {self.reason}")
    