from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # Import User model if it's a custom model

# Create your models here.

# Report model
class Report(models.Model):
    REPORT_TYPES = (
        ('post', 'Post'),
        ('comment', 'Comment'),
    )
    report_type = models.CharField(max_length=7, choices=REPORT_TYPES)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='reports', null=True, blank=True)
    comment = models.ForeignKey('comments.Comment', on_delete=models.CASCADE, related_name='reports', null=True, blank=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)