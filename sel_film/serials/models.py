from django.db import models
from django.urls import reverse

from films.models import gen_slug


class Serial(models.Model):
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    start_year = models.IntegerField()
    end_year = models.IntegerField(blank=True, null=True)
    duration = models.IntegerField()
    rating = models.CharField(max_length=5)
    genres = models.ManyToManyField('Genre', related_name='films', blank=True)
    countries = models.ManyToManyField('Country', related_name='films', blank=True)
    directors = models.ManyToManyField('Director', related_name='films', blank=True)
    actors = models.ManyToManyField('Actor', related_name='films', blank=True)
    plot = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='serials/', blank=True, null=True)
    seasons = models.IntegerField(blank=True, null=True)
    series = models.IntegerField(blank=True, null=True)
    end_status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}. {self.title_ru}'

    def get_absolute_url(self):
        return reverse('serial-detail', kwargs={'pk': self.pk})


class Country(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'


class Genre(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.id:
            if self.last_name:
                self.slug = gen_slug(self.first_name + ' ' + self.last_name)
            else:
                self.slug = gen_slug(self.first_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Director(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.id:
            if self.last_name:
                self.slug = gen_slug(self.first_name + ' ' + self.last_name)
            else:
                self.slug = gen_slug(self.first_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
