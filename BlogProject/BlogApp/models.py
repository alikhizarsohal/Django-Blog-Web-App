from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Custom User model
class User(AbstractUser):
    email_confirmed = models.BooleanField(default=True)
    confirmation_sent_at = models.DateTimeField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    failed_login_attempts = models.IntegerField(default=0)
    lockout_until = models.DateTimeField(null=True, blank=True)

    def reset_failed_login_attempts(self):
        self.failed_login_attempts = 0
        self.save()

    def increment_failed_login_attempts(self):
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            self.lockout_until = timezone.now() + timezone.timedelta(minutes=5)
        self.save()

# Post model
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

# PostAttachment model
class PostAttachment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='post_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

# Comment model
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)

# CommentAttachment model
class CommentAttachment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='comment_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

# Suggestion model
class Suggestion(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='suggestions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='suggestions')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status_choices = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    )
    status = models.CharField(max_length=10, choices=status_choices, default='pending')

# Report model
class Report(models.Model):
    REPORT_TYPES = (
        ('post', 'Post'),
        ('comment', 'Comment'),
    )
    report_type = models.CharField(max_length=7, choices=REPORT_TYPES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reports', null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='reports', null=True, blank=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

