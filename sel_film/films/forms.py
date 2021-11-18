from django import forms

from .models import Film


class FilmForm(forms.Form):
    id = forms.IntegerField()

