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
from database.forms import CreateUserForm, AccountUpdateForm, StudiesForm #createrform imported from forms.py

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

def loginPage(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect('visitor')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')            
            password = request.POST.get('password')
                                         
            user = authenticate(request, username=username, password=password)
            
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


def edit_profile_page(request):
	if not request.user.is_authenticated:
		return redirect("login")
	
	user_id = request.user.id #id of user
	account = Users.objects.get(pk=user_id) #from database

	if account.pk != request.user.pk: #comparison of database pk vs logged in user pk
		return HttpResponse("You cannot edit someone elses profile.")
	context = {}
	if request.POST:
		form = AccountUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save() #apply form save function
			new_username = form.cleaned_data['username']
			return redirect('visitor')
		else:
			form = AccountUpdateForm(request.POST, instance=request.user,
				initial={					
					"email": account.email, 
					"username": account.username,
					"first_name": account.first_name,
					"last_name": account.last_name
				}
			)
			context['form'] = form
	else:
		# display user properties on edit page
		form = AccountUpdateForm(
			initial={					
					"email": account.email, 
					"username": account.username,
					"first_name": account.first_name,
					"last_name": account.last_name
			}
		)
		context['form'] = form
	
	return render(request, 'database/edit_profile_page.html', context)


def add_study(request):
    form = StudiesForm()
    if request.method == 'POST':
        form = StudiesForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'database/add_study.html', context)