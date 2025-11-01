from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # ✅ Import your custom user model

class SignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser  # ✅ Change from User to CustomUser
        fields = ['username', 'email', 'password1', 'password2']
