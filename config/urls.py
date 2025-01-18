"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_PAGE, name='Login'),
    path('logout/', views.logout_PAGE, name='logout'),
    path('login-signup/', views.login_signup_prompt, name='login_signup_prompt'),

    # Logout confirmation page
    path('logout/confirmation/', views.logout_confirmation, name='logout_confirmation'),
    # Referencing logout_PAGE for actual logout
    path('logout/execute/', views.logout_PAGE, name='logout'),

    # For trey to be able to only delete posts
    path('post/<int:pk>/delete/', views.delete_post_confirmation, name='delete_post'),
    
    # Block and unblock user, assign/remove moderator
    path('block_user/<str:username>/', views.block_user, name='block_user'),
    path('unblock_user/<str:username>/', views.unblock_user, name='unblock_user'),
    path('assign_moderator/<str:username>/', views.assign_moderator, name='assign_moderator'),
    path('remove_moderator/<str:username>/', views.remove_moderator, name='remove_moderator'),

    # Post confirmation for deletion
    path('post/delete/confirmation/<int:post_id>/', views.delete_post_confirmation, name='delete_post_confirmation'),

    # Registration
    path('register/', views.register_PAGE, name='register'),

    # Post list and details
    path('post/', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('post/new/', views.create_post, name='create_post'),

    # Profile views
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),  # Updated edit profile URL
]
