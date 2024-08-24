from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # Import User model if it's a custom model

class Post(models.Model):
    author = models.ForeignKey('BlogApp.User', related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

class PostAttachment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='post_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
