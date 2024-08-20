from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-post/', views.create_post, name='create_post'),
    path('posts/', views.post_list, name='post_list'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/report/', views.report_post, name='report_post'),
    path('post/<int:post_id>/suggest/', views.suggest_post, name='suggest_post'),
    path('comment/<int:comment_id>/like/', views.like_comment, name='like_comment'),
    path('comment/<int:comment_id>/reply/', views.reply_to_comment, name='reply_to_comment'),
    path('comment/<int:comment_id>/report/', views.report_comment, name='report_comment'),
    # Include other URL patterns
]