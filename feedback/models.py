from django.db import models
from accounts.models import Customer
from django.utils import timezone
from django.db.models.signals import post_delete
from django.dispatch import receiver

from accounts.models import Customer
from menu.models import FoodItem

# Create your models here.

class FoodItemFeedback(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE, null = True)
    comment = models.CharField(default = '', max_length = 20, blank = True)
    image = models.ImageField(upload_to = 'feedback_imgs/')
    rating = models.SmallIntegerField(default = 1, choices = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], blank = True)
    food_item = models.ForeignKey(FoodItem, on_delete = models.CASCADE, null = True)
    date = models.DateTimeField(auto_now_add = True)

@receiver(post_delete, sender = FoodItemFeedback)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)