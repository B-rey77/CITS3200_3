from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from database.models import Users # Custom user form imported from models.py

# User form - imported from models
class CreateUserForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text="Required. Add a valid email.")
    
    class Meta:
        model = Users
        fields = ('username', 'email', 'first_name', 'last_name', 'about', 'password1', 'password2')
    
    # Verify email if existing
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Users.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"Email {email} is already in use.")

    # Verify username if existing
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Users.objects.get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"Username {username} is already in use.")    
    