from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    context = {"title": "home-page", "description": "this is a home page of ai app"}
    messages.success(request, f"you have successfully logged in mr:{request.user}")
    return render(request, "core/home.html", context)


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "you are successfully registered")
            return redirect("core:login")
        else:
            messages.error(request, "something is error find the err")
    form = UserCreationForm()
    return render(request, "core/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "you have successfully logged in")
            return redirect("core:home")
        else:
            messages.error(request, "username or password are incorrect...")
    return render(request, "core/login.html")


@login_required(login_url="core:login")
def logout_view(request):
    logout(request)
    messages.success(request, "successfully logout you are")
    return redirect("core:home")
