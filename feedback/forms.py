from django import forms
from . import models

class FoodItemFeedback_Form(forms.ModelForm):
    class Meta:
        model = models.FoodItemFeedback
        fields = ['comment', 'image', 'food_item']