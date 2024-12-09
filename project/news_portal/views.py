
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView )
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils import timezone
from .models import Post, UsersSubscribed
from .filters import NewsFilter
from .forms import PostForm, CategoryForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import QuerySet
from django.db.models.signals import post_save



class PostsList(ListView):
    model = Post
    ordering = 'text'
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = ['-date_in']
    paginate_by = 10


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
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class CreateNews(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news_portal.add_post',)

    form_class = PostForm
    model = Post
    template_name = 'post_add.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user # Передаем текущего пользователя в форму
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

            post_save.send(sender=Post, instance=post, created=True, full_url=full_url, email=email)
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
        if UsersSubscribed.objects.filter(user=user, category=category).exists():
            messages.info(self.request, f"Вы уже подписаны на {category}.")
        else:
            subscription = form.save(commit=False)
            subscription.user = user  # Назначаем пользователя подписке
            subscription.save()  # Сохраните экземпляр подписки
            messages.success(self.request, f"Подписка на {category} успешно добавлена.")
        return HttpResponseRedirect(self.request.path)

