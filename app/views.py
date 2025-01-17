from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Post, Comment, UserProfile
from .forms import PostForm, CommentForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test


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
        login(request, user)
        messages.success(request, "Account created successfully!")
        return redirect('post_list')

    return render(request, 'register.html')

def profile_view(request):
    
    user = get_object_or_404(User, username=request.user.username)
    print(f"USER {user}")
    profile = UserProfile.objects.filter(user=user).first()
    posts = Post.objects.filter(author=user).order_by('-created_at')
    return render(request, 'profile.html', {'profile': profile, 'posts': posts})

@login_required
def edit_profile(request):
    print("here")
    user = get_object_or_404(User, username=request.user.username)
    print(f"User {request.user}")
    profile = get_object_or_404(UserProfile, user=request.user)
    print("here again")
    if request.method == 'POST':

        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile', username=request.user.username)
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
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user  # Assign the logged-in user
            new_comment.save()
            return redirect('post_detail', pk=post.pk)

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

@login_required
def delete_post_confirmation(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author and not request.user.is_superuser:
        return redirect('post_list')
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'delete_post_confirmation.html', {'post': post})




#FOR USER MANAGEMENT
def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def user_management(request):
    print("User management view accessed") #Devbug
    users = User.objects.all()
    return render(request, 'user_management.html', {'users': users})


@user_passes_test(is_superuser)
def create_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'create_user.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'create_user.html')

        user = User.objects.create_user(username=username, password=password)
        messages.success(request, "Account created successfully!")
        return redirect('user_management')
    

@user_passes_test(is_superuser)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Ensure user exists
    user.delete()  # Delete the user
    messages.success(request, f'User {user.username} has been deleted.')
    return redirect('user_management')


def login_signup_prompt(request):
    return render(request, 'login_signup_prompt.html')