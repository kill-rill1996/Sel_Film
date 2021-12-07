from django import forms

from .models import Film


class FilmForm(forms.Form):
    title_ru = forms.CharField()
