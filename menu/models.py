from django.db import models
from accounts.models import Customer
from django.utils import timezone
from django.db.models.signals import post_delete
from django.dispatch import receiver
from customer.models import Coupon

# Create your models here.

class FoodItem(models.Model):
    name = models.CharField(default = '', max_length = 20)
    description = models.TextField(default = '')
    image = models.ImageField(upload_to = 'food_imgs/')
    rating = models.DecimalField(default = 3, max_digits = 3, decimal_places = 2)
    is_hot = models.BooleanField(default = False)
    is_recommended = models.BooleanField(default = False)
    is_veg = models.BooleanField(default = True)
    food_category = models.CharField(choices = [('MC', 'Main Course'), ('DE', 'Dessert'), ('BR', 'Bread'), ('SN', 'Snacks')], default = 'MC', max_length = 10)
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
    reservation = models.BooleanField(default = False)
    reservation_price = models.FloatField(default = 0)
    membership_discount = models.FloatField(default = 0)
    coupon = models.OneToOneField(Coupon, on_delete = models.SET_NULL, null = True, blank = True)
    coupon_discount = models.FloatField(default = 0)

class OrderItem(models.Model):
    food_item = models.ForeignKey(FoodItem, on_delete = models.CASCADE, null = True)
    order = models.ForeignKey(Order, on_delete = models.CASCADE, null = True)
    quantity = models.SmallIntegerField(default = 0)

@receiver(post_delete, sender = FoodItem)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)