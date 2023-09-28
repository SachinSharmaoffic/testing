from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # Correct the typo: 'mdoel' to 'model'
        fields = ['content']  # Remove 'name' field if it's not part of your Comment model
        
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),  # Correct the field name: 'body' to 'content'
        }