from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from reviews.models import User


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
