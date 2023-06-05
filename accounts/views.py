from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        
        if (password == confirm_password):
            User.objects.create_user(username=username, password=password)
            return redirect("login")
        else:
            error_message = "Passwords do not match"
            return render(request, "accounts/register.html", {"error_message": error_message})
    
    return render(request, "accounts/register.html")

def user_login(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            error_message = "Invalid username or password"
            return render(request, "accounts/login.html", {"error_message": error_message})
        
    return render(request, "accounts/login.html")

def user_logout(request):
    logout(request)
    return redirect("login")

        
