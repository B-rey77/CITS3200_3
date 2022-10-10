from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from database.models import Studies 

from database.models import Users # Custom user form imported from models.py

# User form - imported from models
class CreateUserForm(UserCreationForm):
	email = forms.EmailField(max_length=255, help_text="Required. Add a valid email.")
	
	class Meta:
		model = Users
		fields = ('email', 'first_name', 'last_name', 'profession', 'country', 'institution', 'password1', 'password2')
	
	# Verify email if existing
	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		try:
			account = Users.objects.get(email=email)
		except Exception as e:
			return email
		raise forms.ValidationError(f"Email {email} is already in use.")    


# form to update user account properties 
class AccountUpdateForm(forms.ModelForm):

	class Meta:
		model = Users
		fields = ('email', 'first_name', 'last_name', 'profession', 'country', 'institution')

	# check if email is valid 
	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		try:
			account = Users.objects.exclude(pk=self.instance.pk).get(email=email)
		except Users.DoesNotExist:
			return email
		raise forms.ValidationError(f'Email {email} is already in use.')

	# Handle saving of updted user properties form
	def save(self, commit=True):
		account = super(AccountUpdateForm, self).save(commit=False)
		account.email = self.cleaned_data['email'].lower()
		account.first_name = self.cleaned_data['first_name']
		account.last_name = self.cleaned_data['last_name']
		account.profession = self.cleaned_data['profession']
		account.country = self.cleaned_data['country']
		account.institution = self.cleaned_data['institution']
		if commit:
			account.save()
		return account
	
class StudiesForm(forms.ModelForm):
	class Meta:
		model = Studies
		fields = '__all__'
