from django.urls import path

from . import views

urlpatterns = [
    path("", views.base, name="base"),
    path('role/admin/', views.role_admin, name='role_admin'),
    path('role/moderator/', views.role_moderator, name='role_moderator'),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path(
        "confirm-email/<uidb64>/<token>/",
        views.confirm_email,
        name="confirm_email"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("moderator/", views.moderator, name="moderator"),
    path(
        "account/dashboard/suggestions/",
        views.jump_to_suggestions,
        name="jump_to_suggestions",
    ),
    path(
        "account/dashboard/posts/",
        views.jump_to_posts,
        name="jump_to_posts"),
    # path('comment/<int:comment_id>/report/', views.report_comment, name='report_comment'), path('suggestions/', suggestion_views.user_suggestions, name='user_suggestions'),
]
