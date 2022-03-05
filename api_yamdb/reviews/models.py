from django.contrib.auth.models import AbstractUser
from django.core.validators import (RegexValidator, MinValueValidator,
                                    MaxValueValidator)
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
        unique=True, blank=False, null=False, verbose_name='Имя пользователя')
    email = models.EmailField(
        max_length=254, unique=True, blank=False,
        null=False, verbose_name='Email')
    bio = models.TextField(max_length=500, blank=True, verbose_name='О себе')
    role = models.CharField(
        max_length=50, choices=ROLES, default=USER, verbose_name='Роль')

    class Meta:
        ordering = ['username']
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    year = models.IntegerField(db_index=True)
    description = models.TextField()
    genre = models.ManyToManyField(
        Genre,
        related_name="titles",
        verbose_name="жанр",
        db_index=True)
    category = models.ForeignKey(
        Category,
        related_name="titles",
        verbose_name="категория",
        db_index=True,
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField('Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор'
    )
    score = models.IntegerField(
        'оценка',
        validators=[
            MinValueValidator(1, 'Минимальная оценка 1'),
            MaxValueValidator(10, 'Максимальная оценка 10')
        ]
    )
    pub_date = models.DateTimeField('дата публикации', auto_now_add=True)
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='one_review')]

    def __str__(self):
        return self.text[:50]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='отзыв'
    )
    text = models.TextField('текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор'
    )
    pub_date = models.DateTimeField('дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:50]
