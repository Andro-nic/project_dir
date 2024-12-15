from django import forms
from django.core.exceptions import ValidationError
from .models import Post, UsersSubscribed, Category
from .templatetags.bad_words import BED_WORDS


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = ['title', 'text', 'author', 'category']
        print(fields)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Получаем пользователя из kwargs
        super().__init__(*args, **kwargs)
        if user:
            self.fields['author'].queryset = self.fields['author'].queryset.filter(user_id=user.id)


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


class CategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        user_category = UsersSubscribed.objects.filter(user=self.user).values_list('category_id', flat=True)
        self.fields['category'].queryset = Category.objects.exclude(id__in=user_category )

    class Meta:
        model = UsersSubscribed
        fields = ['category']
        print(fields)