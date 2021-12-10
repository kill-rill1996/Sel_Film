from django import forms



class Film1FindForm(forms.Form):
    film_1_title_ru = forms.CharField()

    def clean_film_1_title_ru(self):
        data = self.cleaned_data['film_1_title_ru']
        return data.lower()


class Film2FindForm(forms.Form):
    film_2_title_ru = forms.CharField()

    def clean_film_2_title_ru(self):
        data = self.cleaned_data['film_2_title_ru']
        return data.lower()