from django.contrib import admin
from .models import Post, Category, Author


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_category', 'author', 'date_in', 'post_type', 'post_rate')
    list_filter = ('category', 'author', 'date_in')
    search_fields = ('title', 'text')

    def get_category(self, obj):
        return ", ".join([category.category_name for category in obj.category.all()])

    get_category.short_description = 'Category'


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'rate')
    list_filter = ('user', 'rate')
    search_fields = ('user__username', 'user__last_name', 'get_post')


class CategoryAdmin(admin.ModelAdmin):

    list_display = ('category_name', 'subscriber_count')


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
