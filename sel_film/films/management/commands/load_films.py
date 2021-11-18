from django.core.management.base import BaseCommand
import json
from films.models import Film
from django.core.files import File


class Command(BaseCommand):
    help = 'Load films from json file to db'

    def handle(self, *args, **kwargs):
        with open('data/films_info.json', 'r') as file:
            objects = json.loads(file.read())
        for film in objects[:10_000]:
            f = Film.objects.create(
                title_ru=film['title_ru'],
                title_en=film['title_en'],
                year=film['year'],
                duration=film['duration'],
                genres=', '.join(film['genres']),
                countries=', '.join(film['countries']),
                directors=', '.join(film['directors']),
                actors=', '.join(film['actors']),
                plot=film['plot'],
                rating=film['rating']
            )
            f.image.save(f'film_{film["id"]}.jpeg', get_image(film["id"]))
            if film['id'] % 100 == 0:
                print(f'Записан фильм номер {film["id"]}')

    print('Фильмы успешно записаны в базу данных')


def get_image(id):
    return File(open(f'data/posters/films/film_{id}.jpeg', 'rb'))