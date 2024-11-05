from django.urls import path

from . import views

app_name = "comments"

urlpatterns = [
    path(
        "comment/<int:comment_id>/like/",
        views.like_comment,
        name="like_comment"),
    path(
        "comment/<int:comment_id>/reply/",
        views.reply_to_comment,
        name="reply_to_comment",
    ),
    path(
        "my-comments/",
        views.user_comments_view,
        name="user_comments"),
]
