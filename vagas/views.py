from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
import users.form as users

@login_required(login_url='/login')
def index(request):
    return render(request, 'base.html')

def login_manager(request):
    return render(request, 'login.html', {"form": users.LoginForm})

def check_login_valid(request):
    email = request.POST["email"]
    password = request.POST["password"]
    user_login = None
    users = User.objects.all()

    for count, user in enumerate(users):
        if user.email == email:
            user_login = user
        elif count+1 == len(users) and user_login == None:
            messages.add_message(request, messages.ERROR, 'Login ou senha invalidos!')
            return HttpResponseRedirect(reverse('login'))
    user = authenticate(request, username=user_login.username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        messages.add_message(request, messages.ERROR, 'Login ou senha invalidos!')
        return HttpResponseRedirect(reverse('login'))

@login_required(login_url='/login')
def logout_manager(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))
