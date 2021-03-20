from django.db import models
from accounts.models import Customer

# Create your models here.
class Coupon(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE, null = True)
    percentage = models.FloatField(default = 0)
    def __str__(self):
        return f"{self.percentage:.2f}% Discount Coupon"