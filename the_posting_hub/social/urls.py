# social/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.dashboard, name='dashboard'),  # main feed/dashboard
    path('create/', views.create_post, name='create_post'),  # create new post
    path('search/', views.search, name='search'),  # search functionality
    path('logout/', views.logout_user, name='logout'),  # logout functionality
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('', views.user_homepage, name='user_homepage'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('view_post/<int:post_id>/', views.view_post, name='view_post'),
    path('drafts/', views.view_drafts_list, name='view_drafts_list'),
    path('edit_draft/<int:draft_id>/', views.edit_draft, name='edit_draft'),
    path('bookmark_post/<int:post_id>/', views.bookmark_post, name='bookmark_post'),
    path('saved_posts/', views.view_saved_posts, name='view_saved_posts'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('user/<int:user_id>/', views.view_profile, name='view_profile'),
    path('report/<int:user_id>/', views.report_user, name='report_user'),
    path('toggle-follow/<int:user_id>/', views.toggle_follow, name='toggle_follow'),
    path('report_post/<int:post_id>/', views.report_post, name='report_post'),
    path('comment/<int:comment_id>/report/', views.report_comment, name='report_comment'),
    path('notifications/', views.view_notifications, name='notifications'),
    path('notifications/clear/', views.clear_all_notifications, name='clear_all_notifications'),
]
