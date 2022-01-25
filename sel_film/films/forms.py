from django import forms

<<<<<<< HEAD
from .models import Comment
=======
from films.models import Review

>>>>>>> 80dad6b20bc813f7242f618897b735890ae8068c

class Film1FindForm(forms.Form):
    film_1_title_ru = forms.CharField(label='', error_messages={'required': 'Заполните поле*'})

    film_1_title_ru.widget.attrs.update({
        'class': 'form__input form-control',
        # 'class': 'bg-gray-50 border border-gray-500 text-indigo-700 sm:text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 placeholder-gray-300 block w-full p-1.5 lg:p-2.5',
        'placeholder': 'Название фильма...',
        'style': 'border: 1px solid #ff55a5;',
    })

    def clean_film_1_title_ru(self):
        data = self.cleaned_data['film_1_title_ru']
        return data.lower()


class Film2FindForm(forms.Form):
    film_2_title_ru = forms.CharField(label='', error_messages={'required': 'Заполните поле*'})

    film_2_title_ru.widget.attrs.update({
        'class': 'form__input form-control',
        # 'class': 'bg-gray-50 border border-gray-500 text-indigo-700 sm:text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 placeholder-gray-300 block w-full p-1.5 lg:p-2.5',
        'placeholder': 'Название фильма...',
        'style': 'border: 1px solid #ff55a5;',
    })

    def clean_film_2_title_ru(self):
        data = self.cleaned_data['film_2_title_ru']
        return data.lower()


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['email', 'text']


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('title', 'email', 'text', 'rating')

