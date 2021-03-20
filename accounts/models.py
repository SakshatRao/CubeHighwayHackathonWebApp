from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, null = True)
    email = models.EmailField(default = '', unique = True)
    age = models.IntegerField(default = 0)
    contact = models.CharField(max_length = 10, default = '')
    points = models.IntegerField(default = 0)
    membership = models.CharField(choices = [('P', 'Platinum'), ('G', 'Gold'), ('S', 'Silver'), ('B', 'Bronze'), ('N', 'None')], default = 'N', max_length = 3)
    membership_disc_appl = models.BooleanField(default = True)
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name