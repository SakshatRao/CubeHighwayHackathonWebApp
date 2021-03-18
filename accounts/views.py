from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, decorators
from django.db import IntegrityError

import datetime

from . import forms
from .models import Customer
from utils.access import http_dict_func, customer_access

def signup_view(request):
    if(request.method == 'POST'):
        user_form = forms.User_Form(request.POST)
        customer_form = forms.Customer_Form(request.POST)
        if(user_form.is_valid() & customer_form.is_valid()):
            user = user_form.save()
            customer = customer_form.save(commit = False)
            customer.user = user
            customer.email = user.email
            try:
                customer.save()
                login(request, user)
                existing_customer = Customer.objects.filter(email = user.email)
                if(len(existing_customer) == 0):
                    new_customer = Customer()
                    new_customer.email = user.email
                else:
                    new_customer = existing_customer[0]
                new_customer.save()
                return redirect('customer:homepage')
            except IntegrityError:
                user.delete()
                return render(request, 'already_exists.html', http_dict_func(request))
    else:
        user_form = forms.User_Form()
        customer_form = forms.Customer_Form()
    http_dict = http_dict_func(request)
    http_dict['user_form'] = user_form
    http_dict['customer_form'] = customer_form
    return render(request, 'accounts/signup.html', http_dict)

# Login Page
def login_view(request):
    if(request.method == 'POST'):
        user_form = AuthenticationForm(data = request.POST)
        if(user_form.is_valid()):
            user = user_form.get_user()
            login(request, user)
            if('next' in request.POST):
                return redirect(request.POST.get('next'))
            else:
                if(user.is_superuser):
                    return redirect('administration:homepage')
                else:
                    return redirect('customer:homepage')
    else:
        user_form = AuthenticationForm()
    http_dict = http_dict_func(request)
    http_dict['user_form'] = user_form
    return render(request, 'accounts/login.html', http_dict)

# Logout Page
@decorators.login_required(login_url = 'homepage')
def logout_view(request):
    assert request.method == 'POST'
    logout(request)
    return redirect('homepage')

# Edit Customer Details Page (Requires customer login)
@customer_access()
def edit_view(request):
    if(request.method == 'POST'):
        user_form = forms.User_Form(request.POST, instance = request.user)
        customer_form = forms.Customer_Form(request.POST, instance = request.user.customer)
        if(user_form.is_valid() & customer_form.is_valid()):
            user = user_form.save()
            customer = customer_form.save(commit = False)
            customer.user = user
            customer.save()
            login(request, user)
            return redirect('customer:homepage')
    else:
        user_form = forms.User_Form(instance = request.user)
        customer_form = forms.Customer_Form(instance = request.user.customer)
    http_dict = http_dict_func(request)
    http_dict['user_form'] = user_form
    http_dict['customer_form'] = customer_form
    return render(request, 'accounts/edit.html', http_dict)