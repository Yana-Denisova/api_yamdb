from django.contrib import admin

from reviews.models import User, Review, Comment


admin.site.register(User)


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
