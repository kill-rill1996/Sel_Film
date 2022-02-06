from django.db import models
from django.utils.text import slugify
from .utils import alphabet
from django.urls import reverse


def gen_slug(s):
    eng_title = ''.join(alphabet.get(c, c) for c in s.lower())
    return slugify(eng_title, allow_unicode=True)


class Film(models.Model):
    title_ru = models.CharField(db_index=True, max_length=255)
    title_en = models.CharField(db_index=True, max_length=255)
    year = models.IntegerField()
    duration = models.IntegerField()
    rating = models.FloatField(blank=True, null=True)
    genres = models.ManyToManyField('Genre', related_name='films', blank=True)
    countries = models.ManyToManyField('Country', related_name='films', blank=True)
    directors = models.ManyToManyField('Director', related_name='films', blank=True)
    actors = models.ManyToManyField('Actor', related_name='films', blank=True)
    plot = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='films/', blank=True, null=True)

    def __str__(self):
        return f'{self.id}. {self.title_ru}'

    def get_absolute_url(self):
        return reverse('film-detail', kwargs={'pk': self.pk})


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


class Comment(models.Model):
    email = models.EmailField()
    date_pub = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', related_name='child_comments', on_delete=models.CASCADE, blank=True, null=True)
    is_child = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}. {self.email}'


class Review(models.Model):
    title = models.CharField(max_length=256)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='reviews')
    rating = models.FloatField()

    def __str__(self):
        return f'Film #{self.film.id} {self.email} - {self.title}'
