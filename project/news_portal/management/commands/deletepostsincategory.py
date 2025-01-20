from django.core.management.base import BaseCommand, CommandError
from news_portal.models import Post, Category


class Command(BaseCommand):
    help = 'Команда для удаления постов в указанной в аргументах категории (ID), '  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    requires_migrations_checks = True  # напоминать ли о миграциях. Если true — то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def add_arguments(self, parser):
        # Добавляем аргумент для ID категории
        parser.add_argument('category_id', type=int, help='ID категории для удаления постов')
    def handle(self, *args, **options):
        # здесь можете писать любой код, который выполнится при вызове вашей команды
        category_id = options['category_id']
        if not Category.objects.filter(id=category_id).exists():
            self.stdout.write(self.style.ERROR('Категория с ID {} не найдена.'.format(category_id)))
            return
        self.stdout.write(
            'Вы действительно хотите удалить все посты для данной категории? yes/no')  # спрашиваем пользователя, действительно ли он хочет удалить все товары
        answer = input()  # считываем подтверждение

        if answer == 'yes':  # в случае подтверждения действительно удаляем все товары
            Post.objects.filter(category=category_id).delete()
            self.stdout.write(self.style.SUCCESS('Посты в категории с ID {} успешно удалены!'.format(category_id)))
            return

