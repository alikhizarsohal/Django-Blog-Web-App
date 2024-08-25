from django.urls import path
from . import views


app_name = 'suggestions'

urlpatterns = [
    path('user_suggestions/reply/', views.submit_reply, name='submit_reply'),
    path('user_suggestions/', views.user_suggestions, name='user_suggestions'),
    path('user_submitted_suggestions/', views.user_submitted_suggestions, name='user_submitted_suggestions'),
]
