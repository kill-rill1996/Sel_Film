from django import forms

from .models import Film


class FilmFindForm(forms.Form):
    film_1_title_ru = forms.CharField()
    film_2_title_ru = forms.CharField()

    def clean_film_1_title_ru(self):
        data = self.cleaned_data['film_1_title_ru']
        return data.lower()

    def clean_film_2_title_ru(self):
        data = self.cleaned_data['film_2_title_ru']
        return data.lower()


