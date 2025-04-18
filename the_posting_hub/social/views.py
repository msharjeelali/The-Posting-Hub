from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
# social/views.py

from django.shortcuts import render

@login_required
def dashboard(request):
    return render(request, 'social/dashboard.html')  # you can create this template later
