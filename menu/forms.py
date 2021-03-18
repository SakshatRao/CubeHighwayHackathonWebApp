from django import forms
from . import models

class OrderItem_Form(forms.ModelForm):
    class Meta:
        model = models.OrderItem
        fields = ['quantity']