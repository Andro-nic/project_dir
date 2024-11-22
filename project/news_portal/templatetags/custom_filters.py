from django import template
from .bad_words import BED_WORDS

register = template.Library()


@register.filter()
def sensor(text):
    if not isinstance(text, str):  # проверяем является ли переменная text строкой(если нет выдаем исключение)
        raise TypeError('Переменная к которой применяется фильтр должна быть строкового типа')
    for word in text.split():
        if word.lower() in BED_WORDS:
            new_word = word[0] + '.' * (len(word)-1)
            text = text.replace(word, new_word)


    return text

