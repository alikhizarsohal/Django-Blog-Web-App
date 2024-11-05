from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()  # Import User model if it's a custom model


class Post(models.Model):
    author = models.ForeignKey(
        "BlogApp.User", related_name="posts", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        User, related_name="liked_posts", blank=True)
    is_published = models.BooleanField(
        default=False)  # New field for approval status
    
    def get_absolute_url(self):
        print("---------------------------------------------------------------")
        return reverse('posts:post_detail', kwargs={'post_id': self.id})


class PostAttachment(models.Model):
    post = models.ForeignKey(
        "Post", on_delete=models.CASCADE, related_name="attachments"
    )
    file = models.FileField(upload_to="post_attachments/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
