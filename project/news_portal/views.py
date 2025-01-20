from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils import timezone
from .models import Post, UsersSubscribed, Category
from .filters import NewsFilter
from .forms import PostForm, CategoryForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import QuerySet
from .tasks import send_new_post
from django.shortcuts import render, get_object_or_404
from django.core.cache import cache


class PostsList(ListView):
    model = Post
    ordering = 'text'
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = ['-date_in']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # Получаем контекст от родительского метода
        context = super().get_context_data(**kwargs)
        # Получаем список категорий
        context['categories'] = Category.objects.all()
        return context


class PostCategory(ListView):
    model = Post
    template_name = 'post_category.html'
    context_object_name = 'posts'

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        posts = Post.objects.filter(category=category)
        return render(request, 'post_category.html', {'category': category, 'posts': posts})


class PostDetailView(DetailView):
    template_name = 'post.html'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта

        obj = cache.get(f'post-{self.kwargs["pk"]}', None)  # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.

        # если объект' нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
            print('*************')
            print(obj)
            print('*************')
        return obj


class PostsDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class SearchNews(ListView):

    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):

        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        print(self.filterset.qs)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        print(context)
        return context


class CreateNews(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news_portal.add_post',)

    form_class = PostForm
    model = Post
    template_name = 'post_add.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Передаем текущего пользователя в форму
        return kwargs

    def form_valid(self, form):
        post = form.save(commit=False)
        user = self.request.user
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timezone.timedelta(days=1)
        news_count_today = Post.objects.filter(author__user=user.id, date_in__range=(today_start, today_end)).count()
        if news_count_today >= 3:
            form.add_error(None, "Вы уже добавили 3 новости сегодня. Попробуйте завтра.")
            return self.form_invalid(form)
        else:
            path_create = self.request.META['PATH_INFO']
            if path_create == '/news/article/create/':
                post.post_type = 'AR'
            post.save()
            category = form.cleaned_data.get('category')
            if isinstance(category, QuerySet):
               category = category.first()
            full_url = self.request.build_absolute_uri(post.get_absolute_url())
            email_list = UsersSubscribed.objects.filter(category_id=category).values_list('user_id__email', flat=True)
            email = list(email_list)

            send_new_post.delay(post.id, full_url, email)
            # post_save.send(sender=Post, instance=post, created=True, full_url=full_url, email=email)
        return super().form_valid(form)


class EditNews(LoginRequiredMixin, UpdateView):

    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    context_object_name = 'post'  # для проверки на авторство публикации в шаблоне


class DeleteNews(LoginRequiredMixin, DeleteView):

    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    context_object_name = 'post'  # для проверки на авторство публикации в шаблоне


class Subscription(LoginRequiredMixin, CreateView):
    form_class = CategoryForm
    model = UsersSubscribed
    template_name = 'subscription.html'

    def form_valid(self, form):
        user = self.request.user
        category = form.cleaned_data.get('category')
        subscription = form.save(commit=False)
        subscription.user = user  # Назначаем пользователя подписке
        subscription.save()  # Сохраните экземпляр подписки
        messages.success(self.request, f"Подписка на {category} успешно добавлена.")
        return HttpResponseRedirect(self.request.path)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
