from django.contrib import admin
from .models import FoodItem, OrderItem, Order

# Register your models here.
admin.site.register(FoodItem)
admin.site.register(OrderItem)
admin.site.register(Order)