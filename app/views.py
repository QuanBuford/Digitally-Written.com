from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Post, Comment, UserProfile
from .forms import PostForm, CommentForm, UserProfileForm
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError


# Home page view
def home(request):
    return render(request, "home.html")

# Login page view
def login_PAGE(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('post_list') 
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

# Register page view
def register_PAGE(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'register.html')

        user = User.objects.create_user(username=username, password=password)
        # Automatically create a UserProfile
        UserProfile.objects.create(user=user)
        login(request, user)
        messages.success(request, "Account created successfully!")
        return redirect('post_list')

    return render(request, 'register.html')

def profile_view(request, username):
    profile = get_object_or_404(UserProfile, user__username=username)
    posts = Post.objects.filter(author=profile.user)  
    
    return render(request, 'profile.html', {'profile': profile, 'posts': posts})




@login_required
def edit_profile(request, username):
    user = get_object_or_404(User, username=username)
    try:
        profile, created = UserProfile.objects.get_or_create(user=user)
    except IntegrityError:
        profile = UserProfile.objects.get(user=user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile_view', username=username)
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})


# Logout page view
def logout_PAGE(request):
    logout(request)
    return redirect('home')

# Logout confirmation page
@login_required
def logout_confirmation(request):
    return render(request, 'logout_confirmation.html')

# Post list view
def post_list(request):
    # Get all users and their posts
    users = User.objects.all()
    user_posts = {}

    for user in users:
        user_posts[user] = Post.objects.filter(author=user).order_by('-created_at')

    return render(request, 'post_list.html', {'user_posts': user_posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user 
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm() 

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    })



# Create post view
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully.')
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})



# Edit post view
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        messages.error(request, 'You are not authorized to edit this post.')
        return redirect('post_list')
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully.')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'post_form.html', {'form': form})


def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')  
    return render(request, 'delete_post_conformation.html', {'post': post})


@login_required
def delete_post_confirmation(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author and not request.user.is_superuser:
        return redirect('post_list')
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'delete_post_conformation.html', {'post': post})



def login_signup_prompt(request):
    return render(request, 'login_signup_prompt.html')


#MODS!!
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

def assign_moderator(request, username):
    user_to_promote = get_object_or_404(User, username=username)

    if request.user.email != "treyshel@gmail.com":
        messages.error(request, "You are not authorized to assign moderators.")
        return redirect('home')

    # Promote to moderator
    user_profile = get_object_or_404(UserProfile, user=user_to_promote)
    user_profile.is_moderator = True
    user_profile.save()

   # Get permission to change user
    content_type = ContentType.objects.get_for_model(User)  
    permission = Permission.objects.get(codename='change_user')  
    user_to_promote.user_permissions.add(permission)

    messages.success(request, f"{username} has been promoted to moderator.")
    return redirect('profile_view', username=user_to_promote.username)


@login_required
def remove_moderator(request, username):
    user_to_demote = get_object_or_404(User, username=username)

    #only 'treyshel@gmail.com' can remove moderators
    if request.user.email != "treyshel@gmail.com":
        messages.error(request, "You are not authorized to remove moderators.")
        return redirect('home')

    # Demote user
    user_profile = get_object_or_404(UserProfile, user=user_to_demote)
    user_profile.is_moderator = False
    user_profile.save()

    messages.success(request, f"{username} is no longer a moderator.")
    return redirect('profile_view', username=user_to_demote.username)


@login_required
def block_user(request, username):
    user_to_block = get_object_or_404(User, username=username)

    # Only 'treyshel@gmail.com' or moderators can block users
    if request.user.email != "treyshel@gmail.com" and not request.user.profile.is_moderator:
        messages.error(request, "You are not authorized to block users.")
        return redirect('home')
    user_profile = get_object_or_404(UserProfile, user=user_to_block)
    user_profile.is_blocked = True
    user_profile.blocked_by = request.user  # Set the user who blocked them
    user_profile.save()

    messages.success(request, f"You blocked {username}.")
    return redirect('profile_view', username=user_to_block.username)



@login_required
def unblock_user(request, username):
    user_to_unblock = get_object_or_404(User, username=username)

    #only 'treyshel@gmail.com' can unblock users!!
    if request.user.email != "treyshel@gmail.com":
        messages.error(request, "You are not authorized to unblock users.")
        return redirect('home')

    # Unblock the user
    user_profile = get_object_or_404(UserProfile, user=user_to_unblock)
    user_profile.is_blocked = False
    user_profile.save()

    messages.success(request, f"{username} has been unblocked.")
    return redirect('profile_view', username=user_to_unblock.username)


#making sure regular users cant access part of the site
def block_check_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.profile.is_blocked:
            return HttpResponseForbidden("You are blocked from accessing this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if user is blocked
            user_profile = get_object_or_404(UserProfile, user=user)
            if user_profile.is_blocked:
                messages.error(request, f"You cannot log in. You have been blocked by Moderator: {user_profile.blocked_by}")
                return redirect('login') 
            else:
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')
    return render(request, 'login.html')







# #FOR USER MANAGEMENT


# def is_superuser(user):
#     return user.is_superuser

# @user_passes_test(is_superuser)
# def user_management(request):
#     print("User management view accessed") #Devbug
#     users = User.objects.all()
#     return render(request, 'user_management.html', {'users': users})


# # @user_passes_test(is_superuser)
# def create_user(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')

#         if password != confirm_password:
#             messages.error(request, "Passwords do not match.")
#             return render(request, 'create_user.html')

#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists.")
#             return render(request, 'create_user.html')

#         user = User.objects.create_user(username=username, password=password)
#         messages.success(request, "Account created successfully!")
#         return redirect('user_management')
    

# @user_passes_test(is_superuser)
# def delete_user(request, user_id):
#     user = get_object_or_404(User, id=user_id)  # Ensure user exists
#     user.delete()  # Delete the user
#     messages.success(request, f'User {user.username} has been deleted.')
#     return redirect('user_management')

