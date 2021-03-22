from django import forms
from . import models

class FoodItemFeedback_Form(forms.ModelForm):
    class Meta:
        model = models.FoodItemFeedback
        fields = ['image', 'food_item', 'comment']
        help_texts = {
            'food_item': ' (Optional since model can infer food item from image!)',
            'comment': ' (Optional)'
        }