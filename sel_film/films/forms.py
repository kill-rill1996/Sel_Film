from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible
from django import forms

from .models import Comment, Review


class Film1FindForm(forms.Form):
    film_1_title_ru = forms.CharField(label='', error_messages={'required': 'Заполните поле*'})

    film_1_title_ru.widget.attrs.update({
        'class': 'form__input form-control',
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


class RecaptchaForm(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible(attrs={'data-theme': 'dark'}))

