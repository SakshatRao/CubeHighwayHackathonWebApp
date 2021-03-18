from django.shortcuts import render, redirect
from utils.access import http_dict_func, customer_access

from menu.models import FoodItem
from . import forms

# Customer Homepage (Requires login)
@customer_access()
def feedback_view(request):
    if(request.method == 'POST'):
        feedback_form = forms.FoodItemFeedback_Form(request.POST, request.FILES)
        if(feedback_form.is_valid()):
            feedback = feedback_form.save(commit = False)
            feedback.customer = request.user.customer
            
            random_food_item = FoodItem.objects.all()[0]
            feedback.food_item = random_food_item
            
            feedback.save()
            return redirect('feedback:thankyou')
    else:
        feedback_form = forms.FoodItemFeedback_Form()
    http_dict = http_dict_func(request)
    http_dict['feedback_form'] = feedback_form
    return render(request, 'feedback/feedback.html', http_dict)

def show_feedback_view(request):
    customer_reviews = list(request.user.customer.fooditemfeedback_set.all())
    print(customer_reviews)
    http_dict = http_dict_func(request)
    http_dict['reviews'] = customer_reviews
    return render(request, 'feedback/show_feedback.html', http_dict)

def thankyou_view(request):
    http_dict = http_dict_func(request)
    return render(request, 'feedback/thankyou.html', http_dict)