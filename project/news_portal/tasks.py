from django.core.mail import send_mail
from django.utils import timezone
from .models import Post, UsersSubscribed
from django.utils import timezone
from .models import Post, UsersSubscribed
from collections import defaultdict

def my_job():
    now = timezone.now()
    last_week = now - timezone.timedelta(days=7)


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
            #print(f'Здравствуйте, {user.username}!\n\nВот новые статьи за последнюю неделю в разделе {category.category_name}:\n\n{post_list}')
            #print(user.email)
        #Отправка письма пользователю
            send_mail(
                'Еженедельная рассылка новых статей',
                f'Здравствуйте, {user.username}!\n\nВот новые статьи за последнюю неделю в разделе {category.category_name}:\n\n{post_list}',
                'AndrSFtest@yandex.com',
                [user.email],
                fail_silently=False,
            )