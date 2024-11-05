from django.contrib.auth import get_user_model
from django.db import models

from posts.models import Post

User = get_user_model()  # Import User model if it's a custom model


class Suggestion(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="suggestions")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="suggestions")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status_choices = (
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    )
    status = models.CharField(
        max_length=10,
        choices=status_choices,
        default="pending")
    reply = models.OneToOneField(
        "SuggestionReply",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="suggestion",
    )


class SuggestionReply(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="suggestion_replies"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
