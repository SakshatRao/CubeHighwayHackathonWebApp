from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models

# Variables fixed for all users
class User_Form(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

# Variables specific to customer
class Customer_Form(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ['age', 'contact']