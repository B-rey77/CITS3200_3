from tkinter import Entry
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages #import for login messages

from django.contrib.auth.decorators import login_required

# Create your views here.
from database.models import * 
from database.forms import CreateUserForm #createrform imported from forms.py

def home(request):
    return render(request, 'database/home.html')

def signupPage(request):
    if request.user.is_authenticated:
        return redirect('visitor')
    else:
        form = CreateUserForm() #createrform imported from forms.py
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
                        
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)            
                
                return redirect('login')
    
    context = {'form': form}
    return render(request, 'database/signup.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('visitor')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password')
                    
            user = authenticate(request, username=username, password=password, email=email,
                                first_name=first_name, last_name=last_name)
            
            if user is not None:
                login(request, user)                
                return redirect('visitor')
            else:
                messages.info(request, 'Username OR Password is incorrect')
            
    return render(request, 'database/login.html')

# Handling of user logging out
def logoutUser(request):
    logout(request)
    return redirect('login')

# Visitor dashboard
# restrict page view to logged in users

@login_required(login_url='login')
def visitor(request):
    return render(request, 'database/userprofile.html')



