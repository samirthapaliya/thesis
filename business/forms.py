# External Import
from django import forms

# Internal Import
from review.models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
        exclude = ['customer', 'business', 'is_active']
