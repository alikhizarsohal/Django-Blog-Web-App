from django.urls import path
from . import views


app_name = 'suggestions'

urlpatterns = [
    path('user_suggestions/', views.user_suggestions, name='user_suggestions'),
   
]
