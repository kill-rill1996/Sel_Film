from django import forms


class Film1FindForm(forms.Form):
    film_1_title_ru = forms.CharField(label='')

    film_1_title_ru.widget.attrs.update({
        'class': 'bg-gray-50 border border-gray-500 text-indigo-700 sm:text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 placeholder-gray-300 block w-full p-2.5 ',
        'placeholder': 'Название фильма...'
    })

    def clean_film_1_title_ru(self):
        data = self.cleaned_data['film_1_title_ru']
        return data.lower()


class Film2FindForm(forms.Form):
    film_2_title_ru = forms.CharField(label='')

    film_2_title_ru.widget.attrs.update({
        'class': 'bg-gray-50 border border-gray-500 text-indigo-700 sm:text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 placeholder-gray-300 block w-full p-2.5 ',
        'placeholder': 'Название фильма...'
    })

    def clean_film_2_title_ru(self):
        data = self.cleaned_data['film_2_title_ru']
        return data.lower()