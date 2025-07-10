from django import forms
from django.contrib.auth.models import User
from .models import Book
import re

from django.contrib.auth import get_user_model

User = get_user_model()
class SignupForm(forms.ModelForm):
    password = forms.CharField(
    widget=forms.PasswordInput(attrs={'class': 'your-input-class', 'id': 'id_password'})
    )
    confirm_password = forms.CharField(
    widget=forms.PasswordInput(attrs={'class': 'your-input-class', 'id': 'id_confirm_password'})
    )

    role = forms.ChoiceField(
        choices=[('admin', 'Admin'), ('user', 'User')],
        widget=forms.RadioSelect(attrs={'class': 'your-radio-class'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'your-input-class'}),
            'last_name': forms.TextInput(attrs={'class': 'your-input-class'}),
            'email': forms.EmailInput(attrs={'class': 'your-input-class'}),
            'username': forms.TextInput(attrs={'class': 'your-input-class'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_pattern = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
        if not email_pattern.match(email):
            raise forms.ValidationError("Please enter a valid email address.")
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered. Please use a different email or try logging in.")
        
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose a different username.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password_pattern = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$')
        if not password_pattern.match(password):
            raise forms.ValidationError(
                "Password must be at least 8 characters and include uppercase, lowercase, and a number."
            )
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')

        if password and confirm and password != confirm:
            self.add_error('confirm_password', "Passwords do not match.")



class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'category', 'description', 'image', 'quantity']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input-field'}),
            'author': forms.TextInput(attrs={'class': 'input-field'}),
            'category': forms.Select(attrs={'class': 'input-field'}),
            'description': forms.Textarea(attrs={'class': 'input-field'}),
            
            'quantity': forms.NumberInput(attrs={'class': 'input-field'}),
        }


  