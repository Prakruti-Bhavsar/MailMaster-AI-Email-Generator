from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout

# Create your views here.
def index(request):
    return render(request, 'myapp/index.html')

# Handle user registration
def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('register')

        # Create a new user
        user = User(username=username, password=make_password(password), email=email)
        user.save()

        messages.success(request, "Registration successful! You can now login.")
        return redirect('/?login=true')

    return render(request, 'myapp/index.html')

# Handle user login
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to home page after successful login
        else:
            messages.error(request, "Invalid username or password")
            return redirect('index')

    return render(request, 'myapp/dashboard.html')

# Handle user logout
def logout_view(request):
    # Django's logout function clears the session
    logout(request)
    # Redirect to the login page after logout
    return redirect('index')  # Replace 'index' with your login page URL name
