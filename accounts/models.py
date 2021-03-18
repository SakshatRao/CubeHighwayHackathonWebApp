from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, null = True)
    email = models.EmailField(default = '', unique = True)
    age = models.IntegerField(default = 0)
    contact = models.CharField(max_length = 10, default = '')
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name