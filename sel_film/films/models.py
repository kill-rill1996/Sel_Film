from django.db import models


class Film(models.Model):
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    year = models.IntegerField()
    duration = models.IntegerField()
    genres = models.CharField(max_length=255, blank=True, null=True)
    countries = models.CharField(max_length=400, blank=True, null=True)
    directors = models.CharField(max_length=400, blank=True, null=True)
    actors = models.TextField(blank=True, null=True)
    plot = models.TextField(blank=True, null=True)
    rating = models.CharField(max_length=5)
    image = models.ImageField(upload_to='films/', blank=True, null=True)

    def __str__(self):
        return f'{self.id}. {self.title_ru}'
