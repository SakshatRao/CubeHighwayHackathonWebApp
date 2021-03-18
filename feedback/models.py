from django.db import models
from accounts.models import Customer
from django.utils import timezone

from accounts.models import Customer
from menu.models import FoodItem

# Create your models here.

class FoodItemFeedback(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE, null = True)
    comment = models.CharField(default = '', max_length = 20)
    image = models.ImageField(upload_to = 'feedback_imgs/')
    rating = models.SmallIntegerField(default = 0, choices = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])
    food_item = models.ForeignKey(FoodItem, on_delete = models.CASCADE, null = True)