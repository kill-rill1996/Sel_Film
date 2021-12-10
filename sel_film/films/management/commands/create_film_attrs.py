from django.core.management.base import BaseCommand
import json

from films.models import Country, Genre, Actor, Director


class Command(BaseCommand):
    help = 'Create Country, Genre, Actor, Director instance for films in DB'

    def handle(self, *args, **options):
        obj_list = ['countries', 'genres', 'actors', 'directors']
        all_films_json = self.get_all_films_from_json()
        objects_set = self.create_obj_set(obj_list, all_films_json)

        self.write_countries_in_db(objects_set)
        self.write_genres_in_db(objects_set)
        self.write_actors_in_db(objects_set)
        self.write_directors_in_db(objects_set)
        print(f'Все модели успешно записаны в базу данных.')

    def get_all_films_from_json(self):
        with open('data/films_info.json', 'r') as file:
            objects = json.loads(file.read())
        return objects

    def create_obj_set(self, obj_list, films):
        set_list = {attr: [] for attr in obj_list}
        for film in films:
            for obj in obj_list:
                for object in film[f'{obj}']:
                        set_list[obj].append(object)
        for k in set_list:
            set_list[k] = set(set_list[k])
        return set_list

    def write_countries_in_db(self, obj_set):
        for country in obj_set['countries']:
            Country.objects.create(title=country)
        print('Объекты стран успешно созданы')

    def write_genres_in_db(self, obj_set):
        for genre in obj_set['genres']:
            Genre.objects.create(title=genre)
        print('Объекты жанров успешно созданы')

    def write_actors_in_db(self, obj_set):
        for actor in obj_set['actors']:
            actor_splited = actor.split()
            if len(actor_splited) == 1:
                Actor.objects.create(first_name=actor_splited[0], last_name='')
            else:
                Actor.objects.create(first_name=actor_splited[0], last_name=' '.join(actor_splited[1:]))
        print('Объекты актеров успешно созданы')

    def write_directors_in_db(self, obj_set):
        for director in obj_set['directors']:
            director_splited = director.split()
            if len(director_splited) == 1:
                Director.objects.create(first_name=director_splited[0], last_name='')
            else:
                Director.objects.create(first_name=director_splited[0], last_name=' '.join(director_splited[1:]))
        print('Объекты режиссеров успешно созданы')
