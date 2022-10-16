from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.views.decorators.csrf import csrf_protect

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages #import for login messages

from django.contrib.auth.decorators import login_required, user_passes_test

from django.core.mail import EmailMessage

from django.contrib import messages #import for login messages

# Create your views here.
from database.models import * 
from database.forms import CreateUserForm, AccountUpdateForm, StudiesForm, ImportDataForm #createrform imported from forms.py

# Prevent usage of browser back button
from django.views.decorators.cache import cache_control
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator

from database.importer import import_methods_results
import io

def home(request):
	return render(request, 'database/home.html')

def activateEmail(request, user, to_email):
    mail_subject = 'Activate your account.'
    message = render_to_string('database/acc_active_email.html', {
		'user': user.first_name,
		'domain': get_current_site(request).domain,
		'uid': urlsafe_base64_encode(force_bytes(user.pk)),
		'token': account_activation_token.make_token(user),
		'protocol': 'https' if request.is_secure() else 'http'
  	})
    email = EmailMessage(subject=mail_subject, body=message, to=[to_email])
    email.content_subtype = "html"
    
    if email.send():
        messages.success(request, f'Please go to your email address inbox and click on received activation link to confirm and complete the registration. Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')

@csrf_protect
def signupPage(request):
	if request.user.is_authenticated:
		return redirect('visitor')
	else:
		form = CreateUserForm() #createrform imported from forms.py
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
						
			if form.is_valid():
				user = form.save(commit=False)
				user.is_active = False
				user.save()
				email = form.cleaned_data.get('email')
				activateEmail(request, user, email)
				return redirect('home')

			else:
				form = CreateUserForm()
				messages.error(request, f'Something went wrong. Please try again. Please do not create an account with an email address you have registered an account with. Ensure you enter first name and last name')
	
	context = {'form': form}
	return render(request, 'database/signup.html', context)

@csrf_protect
# Activate account after receiving email confirmation
def activate(request, uidb64, token):
    User = get_user_model()
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        
        messages.success(request, f'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.error(request, f'Activation link is invalid!')
    return redirect('home')

@csrf_protect
def loginPage(request, *args, **kwargs):
	if request.user.is_authenticated:
		return redirect('visitor')
	else:
		if request.method == 'POST':
			email = request.POST.get('email')
			first_name = request.POST.get('first_name') 
			last_name = request.POST.get('last_name') 
			password = request.POST.get('password')
										
			user = authenticate(request, email=email, first_name=first_name, last_name=last_name, password=password)
			
			if user is not None:
				login(request, user)                
				return redirect('admin:database_studies_changelist')
			else:
				messages.info(request, 'Email OR Password is incorrect')
			
	return render(request, 'database/login.html')

# Handling of user logging out
def logoutUser(request):
	logout(request)
	return redirect('login')

# Visitor dashboard
# restrict page view to logged in users

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def visitor(request):
	return render(request, 'database/userprofile.html')

@login_required(login_url='login')
def database_search(request):
	return render(request, 'database/database_search.html')

# Update user profile properties
@login_required(login_url='login')
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
			new_email = form.cleaned_data['email']
			messages.success(request, f'Your profile has been successfully updated.')
			return redirect('visitor')
		else:
			form = AccountUpdateForm(request.POST, instance=request.user,
				initial={					
					"email": account.email,
					"first_name": account.first_name,
					"last_name": account.last_name,
					"profession": account.profession,
					"institution": account.institution,
					"country": account.country
				}
			)
			context['form'] = form
	else:
		# display user properties on edit page
		form = AccountUpdateForm(
			initial={					
					"email": account.email, 
					"first_name": account.first_name,
					"last_name": account.last_name,
					"profession": account.profession,
					"institution": account.institution,
					"country": account.country
			}
		)
		context['form'] = form
	
	return render(request, 'database/edit_profile_page.html', context)

# password reset request
def password_reset_request(request):
	if request.method == 'POST':
		password_form = PasswordResetForm(request.POST)
		if password_form.is_valid():
			data = password_form.cleaned_data['email']
			to_email = Users.objects.filter(Q(email=data))
			if to_email.exists():
				for user in to_email:
					subject = 'Password reset.'
					message = render_to_string('database/password/password_reset_email.html', {
						'to_email': user.email,
						'user': user.first_name,
						'site_name': 'CITS32_3',
						'domain': get_current_site(request).domain,
						'uid': urlsafe_base64_encode(force_bytes(user.pk)),
						'token': default_token_generator.make_token(user),
						'protocol': 'https' if request.is_secure() else 'http'
  					})
					email = EmailMessage(subject=subject, body=message, to=[user.email])
					email.content_subtype = "html"
					try:
						email.send()
					except:
						return HttpResponse('Invalid Header')
					return redirect('password_reset_done')
			else:
				messages.error(request, f'Problem sending email, check if you typed it correctly.')
				return redirect('password_reset')
		else:
				messages.error(request, f'Problem sending email, check if you typed it correctly.')
				return redirect('password_reset')
	else:
		password_form = PasswordResetForm()
		
	context = {
		'password_form': password_form
	}
	return render(request, 'database/password/password_reset.html', context)

def superuser_required(user):
	return user.is_superuser

@login_required(login_url='login')
@user_passes_test(superuser_required)
def import_data(request):
	form = ImportDataForm()
	res = None
	if request.method == 'POST':
		form = ImportDataForm(request.POST, request.FILES)
		if form.is_valid():
			# import data
			studies_data = form.cleaned_data['studies_file'].read().decode('utf-8', errors='replace')
			results_data = form.cleaned_data['results_file'].read().decode('utf-8', errors='replace')

			studies_stream = io.StringIO(studies_data)
			results_stream = io.StringIO(results_data)

			res = import_methods_results(studies_stream, results_stream)

	return render(request, 'database/import_data.html', context={
		'form': form,
		'results': res,
	})
