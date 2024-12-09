from django_filters import (FilterSet, DateFilter,
                            CharFilter, ModelChoiceFilter)
from django.forms import DateInput
from .models import Author, Category


class NewsFilter(FilterSet):
    title = CharFilter(
        label='Заголовок',
        lookup_expr='iregex'
    )

    author = ModelChoiceFilter(
        empty_label='Все авторы',
        label='Автор',
        queryset=Author.objects.all()
    )

    category = ModelChoiceFilter(
        empty_label='Все категории',
        label='Категории',
        queryset=Category.objects.all()
    )

    date_after = DateFilter(
        field_name='date_in',
        lookup_expr='gte',
        label='Дата публикации',
        widget=DateInput(attrs={'type': 'date'})
    )

