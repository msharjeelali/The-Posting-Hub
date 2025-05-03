# social/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # main feed/dashboard
    path('create/', views.create_post, name='create_post'),  # create new post
    path('search/', views.search, name='search'),  # search functionality
    path('logout/', views.logout_user, name='logout'),  # logout functionality
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post')
]
