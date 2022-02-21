from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Director(models.Model):
    name = models.TextField(max_length=100)

    @property
    def count_movies(self):
        return self.movies.all().count()

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.DurationField(null=True, blank=True, verbose_name='Durations')
    director = models.ForeignKey(Director, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    @property
    def reviews(self):
        review = Review.objects.filter(movie=self)
        return [{'text'} for i in review]

    @property
    def rating(self):
        p = 0

        for i in self.reviews.all():
            p += int(i.stars)
        try:
            ans = p / self.reviews.all().count()
            return ans
        except ZeroDivisionError:
            ans = p / 1
            return ans


class Review(models.Model):
    text = models.TextField(null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, related_name='reviews')
    stars = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=True)

    def __str__(self):
        return self.text


