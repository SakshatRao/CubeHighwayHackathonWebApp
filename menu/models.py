from django.db import models
from accounts.models import Customer
from django.utils import timezone

# Create your models here.

class FoodItem(models.Model):
    name = models.CharField(default = '', max_length = 20)
    description = models.TextField(default = '')
    image = models.ImageField(upload_to = 'food_imgs/')
    rating = models.SmallIntegerField(default = 0, choices = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])
    is_veg = models.BooleanField(default = True)
    food_category = models.CharField(choices = [('ST', 'Starters'), ('MC', 'Main Course'), ('DE', 'Dessert')], default = 'MC', max_length = 10)
    ingredients = models.TextField(default = '')
    price = models.SmallIntegerField(default = 0)
    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE, null = True)
    date = models.DateTimeField(auto_now = True)
    total = models.FloatField(default = 0)
    tax = models.FloatField(default = 0)
    is_paid = models.BooleanField(default = False)
    final_amt = models.FloatField(default = 0)

class OrderItem(models.Model):
    food_item = models.ForeignKey(FoodItem, on_delete = models.CASCADE, null = True)
    order = models.ForeignKey(Order, on_delete = models.CASCADE, null = True)
    quantity = models.SmallIntegerField(default = 0)