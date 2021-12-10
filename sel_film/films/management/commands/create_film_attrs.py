from django.core.management.base import BaseCommand
import json

from films.models import Country, Genre, Actor, Director


class Command(BaseCommand):
    help = 'Create Country, Genre, Actor, Director instance for films in DB'

    def handle(self, *args, **options):
        all_films_json = self.get_all_films_from_json()
        self.write_countries_in_db(all_films_json)
        self.write_genres_in_db(all_films_json)
        self.write_actors_in_db(all_films_json)
        self.write_directors_in_db(all_films_json)
        print('Все модели успешно записаны в базу данных')

    def get_all_films_from_json(self):
        with open('data/films_info.json', 'r') as file:
            objects = json.loads(file.read())
        return objects

    def create_obj_set(self, obj, films):
        obj_list = []
        for film in films:
            for object in film[f'{obj}']:
                obj_list.append(object)
        return set(obj_list)

    def write_countries_in_db(self, all_films):
        for country in self.create_obj_set(obj='countries', films=all_films):
            Country.objects.create(title=country)
        print('Объекты стран успешно созданы')

    def write_genres_in_db(self, all_films):
        for genre in self.create_obj_set(obj='genres', films=all_films):
            Genre.objects.create(title=genre)
        print('Объекты жанров успешно созданы')

    def write_actors_in_db(self, all_films):
        for actor in self.create_obj_set(obj='actors', films=all_films):
            actor_splited = actor.split()
            if len(actor_splited) == 1:
                Actor.objects.create(first_name=actor_splited[0], last_name='')
            else:
                Actor.objects.create(first_name=actor_splited[0], last_name=' '.join(actor_splited[1:]))
        print('Объекты актеров успешно созданы')

    def write_directors_in_db(self, all_films):
        for director in self.create_obj_set(obj='directors', films=all_films):
            director_splited = director.split()
            if len(director_splited) == 1:
                Director.objects.create(first_name=director_splited[0], last_name='')
            else:
                Director.objects.create(first_name=director_splited[0], last_name=' '.join(director_splited[1:]))
        print('Объекты режиссеров успешно созданы')
