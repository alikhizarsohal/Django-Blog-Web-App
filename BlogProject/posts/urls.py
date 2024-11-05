from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    path("create-post/", views.create_post, name="create_post"),
    path("posts/", views.post_list, name="post_list"),
    path("my-posts/", views.my_post_list, name="my_post_list"),
    path("post/<int:post_id>/", views.post_detail, name="post_detail"),
    path("post/<int:post_id>/like/", views.like_post, name="like_post"),
    path("post/<int:post_id>/add_comment/", views.add_comment, name="add_comment"),
    path("post/<int:post_id>/report/", views.report_post, name="report_post"),
    path("post/<int:post_id>/suggest/", views.suggest_post, name="suggest_post"),
    path("edit/<int:post_id>/", views.edit_post, name="edit_post"),
    path("show_likes", views.show_likes, name="show_likes"),
]
