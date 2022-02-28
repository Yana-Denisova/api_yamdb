from django.db import models


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

class Review(models.Model):
    SCORES = [(i, str(i)) for i in range(1, 11)]
    text = models.TextField()
    author = models.ForeignKey(
        CastomUser, on_delete=models.CASCADE, related_name='reviews'
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
        CastomUser, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]
