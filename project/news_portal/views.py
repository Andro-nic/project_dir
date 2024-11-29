# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from .models import Post
from .filters import NewsFilter
from .forms import PostForm
from django.urls import reverse_lazy


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

    def form_valid(self, form):
        post = form.save(commit=False)
        path_create = self.request.META['PATH_INFO']
        if path_create == '/news/article/create/':
                post.post_type = 'AR'
        post.save()
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



