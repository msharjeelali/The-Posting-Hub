# social/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # main feed/dashboard
    path('create/', views.create_post, name='create_post'),  # create new post
]
