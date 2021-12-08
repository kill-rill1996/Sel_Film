from django.core.management.base import BaseCommand
import json

from films.models import Country, Genre, Actor, Director


class Command(BaseCommand):
    help = 'Create Country, Genre, Actor, Director instance for films in DB'

    def handle(self, *args, **options):
        self.write_countries_in_db()
        self.write_genres_in_db()
        self.write_actors_in_db()
        self.write_directors_in_db()
        print('Все модели успешно записаны в базу данных')

    def get_all_films_from_json(self):
        with open('data/films_info.json', 'r') as file:
            objects = json.loads(file.read())
        return objects

    def create_obj_set(self, obj):
        obj_list = []
        films = self.get_all_films_from_json()
        for film in films:
            for object in film[f'{obj}']:
                obj_list.append(object)
        return set(obj_list)

    def write_countries_in_db(self):
        for country in self.create_obj_set('countries'):
            Country.objects.create(title=country)
        print('Объекты стран успешно созданы')

    def write_genres_in_db(self):
        for genre in self.create_obj_set('genres'):
            Genre.objects.create(title=genre)
        print('Объекты жанров успешно созданы')

    def write_actors_in_db(self):
        for actor in self.create_obj_set('actors'):
            actor_splited = actor.split()
            if len(actor_splited) == 1:
                Actor.objects.create(first_name=actor_splited[0])
            else:
                Actor.objects.create(first_name=actor_splited[0], last_name=' '.join(actor_splited[1:]))
        print('Объекты актеров успешно созданы')

    def write_directors_in_db(self):
        for director in self.create_obj_set('directors'):
            director_splited = director.split()
            if len(director_splited) == 1:
                Director.objects.create(first_name=director_splited[0])
            else:
                Director.objects.create(first_name=director_splited[0], last_name=' '.join(director_splited[1:]))
        print('Объекты режиссеров успешно созданы')
