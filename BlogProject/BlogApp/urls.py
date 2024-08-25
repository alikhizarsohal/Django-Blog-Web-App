from django.urls import path
from . import views


urlpatterns = [
    path('', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('confirm-email/<uidb64>/<token>/', views.confirm_email, name='confirm_email'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('moderator/', views.moderator, name='moderator'),


    # path('create-post/', views.create_post, name='create_post'),
    # path('posts/', views.post_list, name='post_list'),
    # path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    # path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    # path('post/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
    # path('post/<int:post_id>/report/', views.report_post, name='report_post'),
    # path('post/<int:post_id>/suggest/', views.suggest_post, name='suggest_post'),


    # path('comment/<int:comment_id>/like/', views.like_comment, name='like_comment'),
    # path('comment/<int:comment_id>/reply/', views.reply_to_comment, name='reply_to_comment'),
    path('account/dashboard/suggestions/',views.jump_to_suggestions,name='jump_to_suggestions'),
    path('account/dashboard/posts/',views.jump_to_posts,name='jump_to_posts'),
    # path('comment/<int:comment_id>/report/', views.report_comment, name='report_comment'), path('suggestions/', suggestion_views.user_suggestions, name='user_suggestions'),
    # Include other URL patterns
]
