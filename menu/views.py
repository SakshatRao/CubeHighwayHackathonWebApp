from django.shortcuts import render, redirect
from utils.access import http_dict_func, customer_access
import numpy as np

from .models import FoodItem, OrderItem, Order

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
    http_dict['food_items'] = food_items
    http_dict['order'] = current_order
    http_dict['order_items'] = current_order_items
    return render(request, 'menu/menu.html', http_dict)

# Food Item Info page
@customer_access()
def item_view(request):
    if(request.method == 'POST'):
        food_id = [x for x in request.POST.keys() if x.startswith('ID_')]
        assert(len(food_id) == 1)
        food_id = int(food_id[0].split('_')[1])
        food_item = FoodItem.objects.filter(id = food_id)[0]
        http_dict = http_dict_func(request)
        http_dict['food_item'] = food_item
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
    current_order_items = list(current_order.orderitem_set.all())
    if(len(current_order_items) > 0):
        http_dict = http_dict_func(request)
        http_dict['order'] = current_order
        http_dict['order_items'] = current_order_items
        return render(request, 'menu/checkout.html', http_dict)

@customer_access()
def payment_view(request):
    current_order = get_current_order(request)
    current_order.is_paid = True
    current_order.save()
    http_dict = http_dict_func(request)
    return render(request, 'menu/payment.html', http_dict)

@customer_access()
def show_orders_view(request):
    customer_orders = list(request.user.customer.order_set.all())
    http_dict = http_dict_func(request)
    http_dict['orders'] = customer_orders
    return render(request, 'menu/show_orders.html', http_dict)