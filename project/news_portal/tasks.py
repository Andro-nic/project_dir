from django.core.mail import send_mail
from django.utils import timezone
from .models import Post, UsersSubscribed
from collections import defaultdict
from datetime import timedelta
from celery import shared_task
from .models import Post
import time

@shared_task
def send_new_post(post_id, full_url, email):

    post = Post.objects.get(id=post_id)
    # print('******************')
    # print(post.title)
    # print(full_url)
    # print(email)
    # print('******************')
    send_mail(
        subject=f'Новый пост: {post.title}',
        message=f'Проверьте новый пост по следующей ссылке: {full_url}',
        from_email='AndrSFtest@yandex.com',
        recipient_list=[email],
    )


def task_every_week():
    now = timezone.now()
   #last_week = now - timezone.timedelta(days=7)
    last_week = now - timedelta(days=7)


# Извлекаем посты за последнюю неделю
    new_posts = Post.objects.filter(date_in__gte=last_week)

# Подготовка словаря, чтобы сопоставить категории с постами
    post_by_category = defaultdict(list)
    for post in new_posts:
        for category in post.category.all():
            post_by_category[category].append(post)

# Проходим по каждой подписке пользователя
    for subscription in UsersSubscribed.objects.select_related('user', 'category').all():
        user = subscription.user
        category = subscription.category

    # Проверка, есть ли новые посты в категории
        if category in post_by_category:
            posts = post_by_category[category]
            post_list = "\n".join([f"- {post.title}" for post in posts])

                    #Отправка письма пользователю
            send_mail(
                'Еженедельная рассылка новых статей',
                f'Здравствуйте, {user.username}!\n\nВот новые статьи за последнюю неделю в разделе {category.category_name}:\n\n{post_list}',
                'AndrSFtest@yandex.com',
                [user.email],
                fail_silently=False,
            )
