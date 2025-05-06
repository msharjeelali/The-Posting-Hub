from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('team/', views.team, name='team'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html',
             email_template_name='users/password_reset_email.html',
             subject_template_name='users/password_reset_subject.txt'
         ), 
         name='password_reset'),
    
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ), 
         name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ), 
         name='password_reset_confirm'),
    
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ), 
         name='password_reset_complete'),       
]
