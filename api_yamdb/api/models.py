from django.db import models


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
