from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import *
from django.views import generic
from django.views.generic import View
from .models import UserInfo
from django.contrib.auth.decorators import login_required

# Views for home, login, logout, signup anf profile pages

def index(request):
    """Return index."""
    return render(request, "user/index.html")

def login_view(request):
    """Login user and redirect to profile page."""
    # If user submits login details
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("profile"))
        # Redirecting to login again if wrong credentials
        else:
            return render(request, "user/login.html", {"message": "Invalid credentials!"})
    # If user arrives at page by clicking a link
    else:
        return render(request, "user/login.html")

@login_required(login_url='login')
def profile_view(request):
    """Display user profile page."""
    try:
        instance = UserInfo.objects.get(user=request.user)

    except UserInfo.DoesNotExist:
        user_info = UserInfo(user=request.user)
        user_info.save()
        instance = UserInfo.objects.get(user=request.user)


    if request.method == "POST":
        profile_form = ProfileForm(request.POST, instance=instance)

        if profile_form.is_valid():
            profile_form.save()
            return HttpResponseRedirect(reverse("profile"))

    context = {
        'name': instance.name,
        'age': instance.age,
        'email': instance.email,
        'college': instance.college,
    }

    return render(request, 'user/profile.html', context, {"message": "Edits made!"})

def logout_view(request):
    """Logout user and return index."""
    logout(request)
    return render(request, "user/index.html", {"message": "Logged Out!"})

def signup_view(request):
    """Register new user."""
    # If user submits sign up details
    if request.method == "POST":
        form = UserForm(request.POST)

        # Ensuring password and confirm password match
        if request.POST["password"] != request.POST["confirm_pass"]:
            return render(request, "user/signup.html", {"message": "Passwords must match!"})

        # Checking if user already exists
        if User.objects.filter(username=request.POST["username"]).exists():
            return render(request, "user/signup.html", {"message": "User already exists!"})

        if form.is_valid():

            # Not saving user to database immediately
            user = form.save(commit=False)

            # Cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Set the submitted password as a hashed value
            user.set_password(password)
            user.save()

            # Returns User objects if credentials are correct
            user = authenticate(request, username=username, password=password)

            user_info = UserInfo(user=user)
            user_info.save()

            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect(reverse("profile"))

            return HttpResponseRedirect(reverse("profile"))

    # If user arrives at page by clicking a link
    else:
        form = UserForm(None)
        return render(request, "user/signup.html", {"form": form})

@login_required(login_url='login')
def edit_view(request):
    """Return edit form."""
    form = ProfileForm(None)
    return render(request, "user/edit.html", {"form": form})

@login_required(login_url='login')
def delete_view(request):
    """"Delete user account and return index."""
    user = User.objects.get(username=request.user)
    logout(request)
    user.delete()
    return render(request, "user/index.html", {"message": 'User account deleted!'})
