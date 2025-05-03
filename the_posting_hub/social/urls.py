# social/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # main feed/dashboard
    path('create/', views.create_post, name='create_post'),  # create new post
    path('search/', views.search, name='search'),  # search functionality
    path('logout/', views.logout_user, name='logout'),  # logout functionality
]
