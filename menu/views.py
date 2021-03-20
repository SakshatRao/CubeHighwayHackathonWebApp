from django.shortcuts import render, redirect
from utils.access import http_dict_func, customer_access
import numpy as np

from .models import FoodItem, OrderItem, Order
from feedback.models import FoodItemFeedback

def get_current_order(request):
    customer_orders = request.user.customer.order_set.all()
    has_unpaid_order = False
    for order in customer_orders:
        if(order.is_paid == False):
            current_order = order
            has_unpaid_order = True
            break
    if(has_unpaid_order == False):
        order = Order(customer = request.user.customer)
        order.save()
        current_order = order
    return current_order

def get_reservation_price():
    return 100

def get_food_from_category(food_items, target_category):
    chosen_foods = []
    for item in food_items:
        if(item.food_category == target_category):
            chosen_foods.append(item)
    return chosen_foods

# Customer Homepage (Requires login)
@customer_access()
def menu_view(request):
    
    food_items = []
    for food_item in FoodItem.objects.all():
        food_item_dict = {}
        food_item_dict['name'] = food_item.name
        food_item_dict['descr'] = food_item.description
        food_item_dict['category'] = food_item.food_category
        food_item_dict['price'] = food_item.price
        food_item_dict['rating'] = food_item.rating
        food_item_dict['is_veg'] = food_item.is_veg
        food_items.append(food_item)
    
    starters = get_food_from_category(food_items, 'ST')
    main_courses = get_food_from_category(food_items, 'MC')
    desserts = get_food_from_category(food_items, 'DE')
    breads = get_food_from_category(food_items, 'BR')
    snacks = get_food_from_category(food_items, 'SN')
    
    customer_orders = request.user.customer.order_set.all()
    has_unpaid_order = False
    for order in customer_orders:
        if(order.is_paid == False):
            current_order = order
            current_order_items = list(order.orderitem_set.all())
            has_unpaid_order = True
            break
    if(has_unpaid_order == False):
        current_order = None
        current_order_items = []

    http_dict = http_dict_func(request)
    http_dict['st_items'] = starters
    http_dict['mc_items'] = main_courses
    http_dict['de_items'] = desserts
    http_dict['br_items'] = breads
    http_dict['sn_items'] = snacks
    http_dict['order'] = current_order
    http_dict['order_items'] = current_order_items
    http_dict['reservation_price'] = get_reservation_price()
    return render(request, 'menu/menu.html', http_dict)

# Food Item Info page
@customer_access()
def item_view(request):
    if(request.method == 'POST'):
        
        food_id = [x for x in request.POST.keys() if x.startswith('ID_')]
        assert(len(food_id) == 1)
        food_id = int(food_id[0].split('_')[1])
        food_item = FoodItem.objects.filter(id = food_id)[0]

        food_reviews = list(FoodItemFeedback.objects.filter(food_item = food_item))
        
        http_dict = http_dict_func(request)
        http_dict['food_item'] = food_item
        http_dict['food_reviews'] = food_reviews
        return render(request, 'menu/item.html', http_dict)

# Order Food Item page
@customer_access()
def order_item_view(request):
    if(request.method == 'POST'):
        
        current_order = get_current_order(request)
        
        qty = int(request.POST['qty'])
        food_id = [x for x in request.POST.keys() if x.startswith('ID_')]
        assert(len(food_id) == 1)
        food_id = int(food_id[0].split('_')[1])
        food_item = FoodItem.objects.filter(id = food_id)[0]
        
        already_present = False
        for order_item in current_order.orderitem_set.all():
            if(order_item.food_item == food_item):
                already_present = True
                order_item.quantity += qty
                order_item.save()
                break
        if(already_present == False):
            order_item = OrderItem(food_item = food_item, order = current_order, quantity = qty)
            order_item.save()
        
        current_order.total += (food_item.price * qty)
        current_order.save()
        
        return redirect('menu:menu')

@customer_access()
def checkout_view(request):
    current_order = get_current_order(request)
    current_order.total = round(current_order.total, 1)
    current_order.reservation_price = round(current_order.reservation_price)
    current_order.tax = round(0.18543 * current_order.total, 1)
    current_order.final_amt = round(current_order.total + current_order.reservation_price + current_order.tax, 0)
    current_order.save()
    current_order_items = list(current_order.orderitem_set.all())
    if(len(current_order_items) > 0):
        http_dict = http_dict_func(request)
        http_dict['order'] = current_order
        http_dict['order_items'] = current_order_items
        return render(request, 'menu/checkout.html', http_dict)

@customer_access()
def payment_view(request):
    current_order = get_current_order(request)
    if(current_order.total > 0):
        current_order.is_paid = True
        current_order.save()
    http_dict = http_dict_func(request)
    return render(request, 'menu/payment.html', http_dict)

@customer_access()
def show_orders_view(request):
    customer_orders = list(request.user.customer.order_set.all())
    customer_orders = [x for x in customer_orders if x.is_paid == True]
    http_dict = http_dict_func(request)
    http_dict['orders'] = customer_orders
    return render(request, 'menu/show_orders.html', http_dict)

@customer_access()
def update_view(request):
    if(request.method == 'POST'):
        
        current_order = get_current_order(request)
        
        action = -1
        for key in request.POST.keys():
            if(key.startswith('ID-_')):
                action = '-'
                break
            elif(key.startswith('ID+_')):
                action = '+'
                break
            elif(key.startswith('IDx_')):
                action = 'x'
                break
        assert(action != -1)

        order_item_id = [x for x in request.POST.keys() if x.startswith(f"ID{action}_")]
        assert(len(order_item_id) == 1)
        order_item_id = int(order_item_id[0].split('_')[1])
        order_item = OrderItem.objects.filter(id = order_item_id)[0]
        
        if(action == '-'):
            if(order_item.quantity > 1):
                order_item.quantity -= 1
                order_item.save()
                current_order.total -= order_item.food_item.price
                current_order.save()
            else:
                current_order.total -= (order_item.food_item.price * order_item.quantity)
                if(current_order.total == 0):
                    current_order.delete()
                else:
                    current_order.save()
                order_item.delete()
        elif(action == '+'):
            order_item.quantity += 1
            order_item.save()
            current_order.total += order_item.food_item.price
            current_order.save()
        else:
            current_order.total -= (order_item.food_item.price * order_item.quantity)
            if(current_order.total == 0):
                current_order.delete()
            else:
                current_order.save()
            order_item.delete()
        
        return redirect('menu:menu')

@customer_access()
def reservation_view(request):
    if(request.method == 'POST'):
        current_order = get_current_order(request)
        if(current_order.reservation == False):
            current_order.reservation = True
            current_order.reservation_price = get_reservation_price()
        else:
            current_order.reservation = False
            current_order.reservation_price = 0
        current_order.save()
        return redirect('menu:menu')