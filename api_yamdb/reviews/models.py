from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'))
    username = models.CharField(
        max_length=150, validators=[RegexValidator(regex=r'^[\w.@+-]+\Z')],
        unique=True, blank=False, null=False)
    email = models.EmailField(
        max_length=254, unique=True, blank=False, null=False)
    bio = models.TextField(max_length=500, blank=True, verbose_name='О себе')
    role = models.CharField(
        max_length=50, choices=ROLES, default=USER, verbose_name='Роль')

    class Meta:
        ordering = ['username']

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
