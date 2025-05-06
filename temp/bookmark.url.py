# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('bookmark/<int:post_id>/', views.toggle_bookmark, name='toggle_bookmark'),
]
