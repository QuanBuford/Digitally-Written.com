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
import app.views
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app.views.home, name='home'),
    path('login/', app.views.login_PAGE, name='Login'),
    path('logout/', app.views.logout_PAGE, name='logout'),
   

    path('login-signup/', app.views.login_signup_prompt, name='login_signup_prompt'),
    # amanda logout confirmation page
    path('logout/confirmation/', app.views.logout_confirmation, name='logout_confirmation'),  

    # amanda to reference logout_PAGE 
    path('logout/execute/', app.views.logout_PAGE, name='logout'),  

    # for trey to be able to only delete posts
    path('post/<int:pk>/delete/', app.views.delete_post_confirmation, name='delete_post'),
    # path('user-management/', app.views.user_management, name='user_management'),
    # path('user/create/', app.views.create_user, name='create_user'),
    # path('user/delete/<int:user_id>/', views.delete_user, name='delete_user'),


    path('post/delete/confirmation/<int:post_id>/', app.views.delete_post_confirmation, name='delete_post_confirmation'),  # This was commented out

    path('register/', app.views.register_PAGE, name='register'),
    
    path('post/', app.views.post_list, name='post_list'),
    path('post/<int:pk>/', app.views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', app.views.edit_post, name='edit_post'),
    path('post/new/', app.views.create_post, name='create_post'),
    path('profile/', app.views.profile_view, name='profile_view'),
    path('edit/', app.views.edit_profile, name='edit_profile'),
]
