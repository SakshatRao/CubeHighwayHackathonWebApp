from django.shortcuts import render, redirect
from utils.access import http_dict_func, customer_access
import numpy as np

from menu.models import FoodItem
from . import forms
from customer.models import Coupon

def random_coupon_gen(customer):
    thresh = 1
    if(np.random.uniform() < thresh):
        coupon = Coupon(customer = customer, percentage = round(np.random.uniform(low = 5, high = 20), 0))
        coupon.save()
        return coupon
    else:
        return None

# Customer Homepage (Requires login)
@customer_access()
def feedback_view(request):
    if(request.method == 'POST'):
        feedback_form = forms.FoodItemFeedback_Form(request.POST, request.FILES)
        if(feedback_form.is_valid()):
            feedback = feedback_form.save(commit = False)
            feedback.customer = request.user.customer
            feedback.rating = int(request.POST['emoji_feedback'])
            feedback.save()
            all_ratings = [x.rating for x in feedback.food_item.fooditemfeedback_set.all()]
            avg_rating = np.mean(all_ratings)
            feedback.food_item.rating = avg_rating
            if(avg_rating >= 4):
                feedback.food_item.is_hot = True
            else:
                feedback.food_item.is_hot = False
            feedback.food_item.save()
            return redirect('feedback:thankyou')
    else:
        feedback_form = forms.FoodItemFeedback_Form()
    http_dict = http_dict_func(request)
    http_dict['feedback_form'] = feedback_form
    return render(request, 'feedback/feedback.html', http_dict)

def show_feedback_view(request):
    customer_reviews = list(request.user.customer.fooditemfeedback_set.all())
    http_dict = http_dict_func(request)
    http_dict['reviews'] = customer_reviews
    return render(request, 'feedback/show_feedback.html', http_dict)

def thankyou_view(request):
    http_dict = http_dict_func(request)
    coupon = random_coupon_gen(request.user.customer)
    http_dict['coupon'] = coupon
    return render(request, 'feedback/thankyou.html', http_dict)