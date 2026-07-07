from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .decorators import admin_required
from .forms import LoginForm

def account_login(request):

    form = LoginForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            login(request, form.user)

            if form.user.role == "admin":
                return redirect("admin_dashboard")

            elif form.user.role == "member":
                return redirect("member_dashboard")
            
    print('form',form.errors)
    return render(request, "account/login.html", {"form": form})

def account_logout(request):

    logout(request)

    return redirect("account_login")

def member_dashboard(request):

    return render(request, "member/dashboard.html")