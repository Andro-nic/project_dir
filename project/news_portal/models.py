from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions import Coalesce
from django.db.models import Sum
from django.urls import reverse
from django.core.cache import cache


class Author(models.Model):
    rate = models.FloatField(default=0.0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        posts_rate = self.post_set.aggregate(pr=Coalesce(Sum('post_rate'), 0))['pr']
        comments_rate = self.user.comment_set.aggregate(cr=Coalesce(Sum('comment_rate'), 0))['cr']
        comments_posts_rate = self.post_set.aggregate(cpr=Coalesce(Sum('comment__comment_rate'), 0))['cpr']
        self.rate = posts_rate * 3 + comments_rate + comments_posts_rate
        self.save()
        return self.rate

    def __str__(self):
        return self.user.username


class Category(models.Model):

    category_name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, related_name='subscribed_categories', through='UsersSubscribed')

    def __str__(self):
        return self.category_name

    def subscriber_count(self):
        return self.subscribers.count()  # Возвращает количество подписчиков


class UsersSubscribed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} is subscribed to category {self.category}'


class Post(models.Model):
    article = 'AR'
    news = 'NW'
    POST_TYPES = [
        (article, 'Статья'),
        (news, 'Новость')
    ]

    text = models.TextField()
    title = models.CharField(max_length=100)
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default='NW')
    date_in = models.DateTimeField(auto_now_add=True)
    post_rate = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.post_rate += 1
        self.save()
        return self.post_rate

    def dislike(self):
        self.post_rate -= 1
        self.save()
        return self.post_rate

    def preview(self):
        return f'{self.text[:124]}...'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField()
    date_in = models.DateTimeField(auto_now_add=True)
    comment_rate = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.comment_rate += 1
        self.save()
        return self.comment_rate

    def dislike(self):
        self.comment_rate -= 1
        self.save()
        return self.comment_rate
