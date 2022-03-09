from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from reviews.models import User, Review, Comment, Title, Genre, Category


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'pub_date', 'title', 'score')
    list_filter = ('pub_date', 'score')
    search_fields = ('text',)
    empty_value_display = '-пусто-'


admin.site.register(Review, ReviewAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'pub_date', 'review')
    list_filter = ('pub_date',)
    search_fields = ('text',)
    empty_value_display = '-пусто-'


admin.site.register(Comment, CommentAdmin)


class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {'fields': ('email', 'password1', 'password2', 'username', 'role')}
        ),
    )
    list_display = ('username', 'email', 'role', 'is_admin')
    list_filter = ('role', )
    search_fields = ('username', 'email')
    ordering = ('username',)


admin.site.register(User, CustomUserAdmin)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'description', 'category')
    list_filter = ('year', 'genre', 'category')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_filter = ('slug', )
    search_fields = ('name',)


admin.site.register(Genre, GenreAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_filter = ('slug', )
    search_fields = ('name',)


admin.site.register(Category, CategoryAdmin)
