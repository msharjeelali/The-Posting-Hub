from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def home(request):
    if request.user.is_authenticated:
        return redirect('feed')
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def team(request):
    return render(request, 'core/team.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})
