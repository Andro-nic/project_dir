from django.urls import path
# Импортируем созданное нами представление
from .views import (PostsList, PostsDetail, SearchNews, CreateNews,
                    EditNews, DeleteNews)


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostsList.as_view(), name='post_list'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', PostsDetail.as_view(), name='post_detail'),
   path('search/',  SearchNews.as_view(), name='search_news'),
   path('create/',  CreateNews.as_view(), name='create_news'),
   path('<int:pk>/edit/', EditNews.as_view(), name='edit_news'),
   path('<int:pk>/delete/', DeleteNews.as_view(), name='delete_news'),
   path('article/create/',  CreateNews.as_view(), name='create_article'),
   path('article/<int:pk>/edit/', EditNews.as_view(), name='edit_article'),
   path('article/<int:pk>/delete/', DeleteNews.as_view(), name='delete_article'),
    ]