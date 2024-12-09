from django.template.loader import render_to_string
from django.dispatch import receiver
from .models import Post
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save



@receiver(post_save, sender=Post)
def notify_managers_news_portal(sender, instance, created, **kwargs):
    full_url = kwargs.get('full_url')
    email = kwargs.get('email')
    print(f'signal {email}')
    html_content = render_to_string(
        'post_created.html',
        {
            'post': instance,
            'full_url': full_url,
        }
    )
    msg = EmailMultiAlternatives(
        subject=instance.title,
        body=instance.text[:50],
        from_email='AndrSFtest@yandex.ru',
        to=email,
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html
    msg.send()


