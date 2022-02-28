from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    USER = 'USER'
    MODERATOR = 'MODERATOR'
    ADMIN = 'ADMIN'
    ROLES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )
    username = models.CharField(
        max_length=150, validators=[RegexValidator(regex=r'^[\w.@+-]+$')],
        unique=True, blank=False, null=False)
    email = models.EmailField(
        max_length=254, unique=True, blank=False, null=False)
    bio = models.TextField(max_length=500, blank=True, verbose_name='О себе')
    role = models.CharField(
        max_length=50, choices=ROLES,
        default=USER, verbose_name='Роль')
    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff
    @property
    def is_moderator(self):
        return self.role == self.MODERATOR or self.is_superuser


class Genres(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Review(models.Model):
    SCORES = [(i, str(i)) for i in range(1, 11)]
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.IntegerField(
        choices=SCORES,
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    title = models.ForeignKey(
        Titles, on_delete=models.CASCADE, related_name='reviews'
    )


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]


class Titles(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    rating = models.ForeignKey(
        Review,
        related_name="rating",
        on_delete=models.CASCADE,
    )
    description = models.TextField()
    genre = models.ForeignKey(
        Genres,
        related_name="genre",
    )
    categorie = models.ForeignKey(
        Categories,
        related_name="categorie",
    )

    def __str__(self):
        return self.name
