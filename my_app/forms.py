from django import forms
from .models import Review, Newsletter

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['author', 'rating', 'text']
        widgets = {
            'author': forms.TextInput(attrs={'placeholder': 'Ваше ім\'я', 'style': 'width: 100%; margin-bottom: 10px; padding: 8px;'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'style': 'width: 100%; margin-bottom: 10px; padding: 8px;'}),
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ваша думка про актив...', 'style': 'width: 100%; margin-bottom: 10px; padding: 8px;'}),
        }

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Ваш email', 'required': True, 'style': 'padding: 10px; border-radius: 5px; border: 1px solid #ccc;'})
        }