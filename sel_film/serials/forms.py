from django import forms

from serials.models import Review


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('title', 'email', 'text', 'rating')