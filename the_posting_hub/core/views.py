from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def team(request):
    return render(request, 'core/team.html')

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # This is actually the email
            password = form.cleaned_data.get('password')
            
            # Get the username from the email
            try:
                user_obj = User.objects.get(email=email)
                username = user_obj.username
            except User.DoesNotExist:
                messages.error(request, "No account found with this email address.")
                return render(request, 'core/login.html', {'form': form})
            
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Display the full name if available, otherwise use email
                display_name = f"{user.first_name} {user.last_name}".strip() or user.email
                messages.success(request, f"Welcome back, {display_name}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid password.")
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'core/login.html', {'form': form})

def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Save the date of birth to the user profile
            profile = user.profile
            profile.date_of_birth = form.cleaned_data.get('date_of_birth')
            profile.save()
            
            login(request, user)
            # Display the full name if available, otherwise use email
            display_name = f"{user.first_name} {user.last_name}".strip() or user.email
            messages.success(request, f"Welcome to The Posting Hub, {display_name}!")
            return redirect('dashboard')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/signup.html', {'form': form})
