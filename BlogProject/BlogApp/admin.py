from django.contrib import admin

from comments.models import Comment, CommentAttachment
from posts.models import Post, PostAttachment
from reports.models import Report
from suggestions.models import Suggestion, SuggestionReply

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "email_confirmed",
        "confirmation_sent_at",
        "profile_picture",
        "failed_login_attempts",
        "lockout_until",
    )
    search_fields = ("username", "email")
    readonly_fields = ("confirmation_sent_at", "lockout_until")
    list_filter = ("email_confirmed", "failed_login_attempts", "lockout_until")
    # Add more configurations if needed


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "created_at",
        "updated_at",
        "is_published",  # Add is_published here
    )
    search_fields = ("title", "content")
    list_filter = (
        "created_at",
        "updated_at",
        "is_published",
    )  # Add is_published here for filtering
    filter_horizontal = ("likes",)  # For ManyToMany fields


@admin.register(PostAttachment)
class PostAttachmentAdmin(admin.ModelAdmin):
    list_display = ("post", "file", "uploaded_at")
    list_filter = ("uploaded_at",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "post",
        "author",
        "content",
        "created_at",
        "parent_comment")
    search_fields = ("content",)
    list_filter = ("created_at", "parent_comment")
    filter_horizontal = ("likes",)  # For ManyToMany fields


@admin.register(CommentAttachment)
class CommentAttachmentAdmin(admin.ModelAdmin):
    list_display = ("comment", "file", "uploaded_at")
    list_filter = ("uploaded_at",)


@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = (
        "post",
        "user",
        "content",
        "status",
        "created_at",
        "modified_at")
    search_fields = ("content",)
    list_filter = ("status", "created_at", "modified_at")


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "report_type",
        "post",
        "comment",
        "reported_by",
        "reason",
        "created_at",
        "is_resolved",
    )
    search_fields = ("reason",)
    list_filter = ("report_type", "created_at", "is_resolved")
    raw_id_fields = (
        "post",
        "comment",
        "reported_by",
    )  # To speed up the admin interface for foreign keys


@admin.register(SuggestionReply)
class SuggestionReplyAdmin(admin.ModelAdmin):
    list_display = ("suggestion", "user", "content", "created_at")
    search_fields = ("content",)
    list_filter = ("created_at",)
