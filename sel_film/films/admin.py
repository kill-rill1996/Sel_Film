from django.contrib import admin
from . import models

admin.site.register(models.Film)
admin.site.register(models.Actor)
admin.site.register(models.Director)


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}