from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User


# Create your views here.

def home(request):
    return render(request, "home.html")


def login_PAGE(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('event_list') 
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

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
        return redirect('Login')

    return render(request, 'register.html')

def logout_PAGE(request):
    logout(request)
    return redirect('home')