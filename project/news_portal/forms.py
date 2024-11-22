from django import forms
from django.core.exceptions import ValidationError
from .models import Post
from .templatetags.bad_words import BED_WORDS


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = ['title', 'text', 'author']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        text = cleaned_data.get('text')
        if text == title:
            raise ValidationError(
                "Содержание и заголовок новости не могут совпадать."
            )
        for word in text.split():
            if word.lower() in BED_WORDS:
                raise ValidationError(
                    "Текст содержит нецензурную лексику."
                )
            break
        for word in title.split():
            if word.lower() in BED_WORDS:
                raise ValidationError(
                    "Заголовок публикации содержит нецензурную лексику."
                )
            break

        return cleaned_data
