from django.core.management.base import BaseCommand
from django.core.files import File
import json

from films.models import Film, Country, Genre, Actor, Director


class Command(BaseCommand):
    help = 'Create films instance in DB'

    def handle(self, *args, **kwargs):
        error_films = []
        films = self.get_all_films_from_json()
        for film in films[:500]:
            f = Film.objects.create(
                title_ru=film['title_ru'],
                title_en=film['title_en'],
                year=film['year'],
                duration=film['duration'],
                plot=film['plot'],
            )
            if film['rating']:
                f.rating = float(film['rating'])
            # adding poster
            f.image.save(f'film_{film["id"]}.jpeg', self.get_image(film["id"]))

            # adding countries
            for country in self.get_attr_for_creating('countries', film, Country):
                f.countries.add(country)

            # adding genres
            for genre in self.get_attr_for_creating('genres', film, Genre):
                f.genres.add(genre)

            # adding actors
            for actor in self.get_attr_for_creating('actors', film, Actor):
                f.actors.add(actor)

            # adding directors
            try:
                for director in self.get_attr_for_creating('directors', film, Director):
                    f.directors.add(director)
            except Exception as e:
                error_films.append(f'{f.id}. {f.title_ru} - {e} (Режиссеры)')

            # мониторинг создания фильмов
            if film['id'] % 10 == 0:
                print(f'Записан фильм номер {film["id"]}')

        for film in error_films:
            print(film)

    def get_attr_for_creating(self, attr, film, model):
        inst_list = []

        for obj in film[attr]:
            if model in (Actor, Director):
                obj_splited = obj.split()
                if len(obj_splited) == 1:
                    inst = model.objects.filter(first_name=obj_splited[0], last_name='')[0]
                else:
                    inst = model.objects.filter(first_name=obj_splited[0], last_name=' '.join(obj_splited[1:]))[0]
            else:
                inst = model.objects.get(title=obj)
            inst_list.append(inst)
        return inst_list

    def get_all_films_from_json(self):
        with open('data/films_info.json', 'r') as file:
            objects = json.loads(file.read())
        return objects

    def get_image(self, id):
        return File(open(f'data/posters/films/film_{id}.jpeg', 'rb'))