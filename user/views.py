from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from basic.models import Category
from .forms import SignUpForm
from .models import Profile


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'User successfully register!')
            return redirect('index')
        else:
            messages.warning(request, form.errors)
            return redirect('register')
    form = SignUpForm()
    return render(request, 'user/register.html', {'form': form})


def login_(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            messages.warning(request, 'Login error')
            return redirect('login')
    return render(request, 'user/login.html')


def logout_(request):
    logout(request)
    return redirect('index')


@login_required(login_url='login/')
def user_home(request):
    user = Profile.objects.get(user=request.user)
    catgory = Category.objects.all()
    return render(request, 'user/user_home.html', {'user': user, 'category': catgory})
