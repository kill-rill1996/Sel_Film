from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible

from serials.models import Review, Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('email', 'text')


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('title', 'email', 'text', 'rating')


class RecaptchaForm(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible(attrs={'data-theme': 'dark'}))