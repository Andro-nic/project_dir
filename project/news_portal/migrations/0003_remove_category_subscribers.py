# Generated by Django 5.1.2 on 2024-12-09 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news_portal', '0002_category_subscribers_userssubscribed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='subscribers',
        ),
    ]
