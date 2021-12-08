from django.core.management.base import BaseCommand
from django.core.files import File
import json

from serials.models import Serial, Country, Genre, Actor, Director


class Command(BaseCommand):
    help = 'Create films instance in DB'

    def handle(self, *args, **kwargs):
        serials = self.get_all_serials_from_json()

        for serial in serials[:50]:
            f = Serial.objects.create(
                title_ru=serial['title_ru'],
                title_en=serial['title_en'],
                start_year=2000,
                end_year=2001,
                duration=serial['duration'],
                rating=serial['rating'],
                plot=serial['plot'],
                seasons=serial['seasons'],
                series=serial['series'],
                end_status=self.get_end_status(serial['end_status']),
            )

            # adding poster
            f.image.save(f'film_{serial["id"]}.jpeg', self.get_image(serial["id"]))

            # adding countries
            for country in self.get_attr_for_creating('countries', serial, Country):
                f.countries.add(country)

            # adding genres
            for genre in self.get_attr_for_creating('genres', serial, Genre):
                f.genres.add(genre)

            # adding actors
            for actor in self.get_attr_for_creating('actors', serial, Actor):
                f.actors.add(actor)

            # adding directors
            for director in self.get_attr_for_creating('directors', serial, Director):
                f.directors.add(director)

            # мониторинг создания сериалов
            if serial['id'] % 10 == 0:
                print(f'Записан сериал номер {serial["id"]}')

    def get_attr_for_creating(self, attr, serial, model):
        inst_list = []

        for obj in serial[attr]:
            if model in (Actor, Director):
                obj_splited = obj.split()
                if len(obj_splited) == 1:
                    model.objects.get(first_name=obj_splited[0], last_name=None)
                else:
                    inst = model.objects.get(first_name=obj_splited[0], last_name=' '.join(obj_splited[1:]))
            else:
                inst = model.objects.get(title=obj)
            inst_list.append(inst)
        return inst_list


    def get_end_status(self, status):
        if status:
            return True
        return False

    def year_split(self, year):
        pass

    def get_all_serials_from_json(self):
        with open('data/serials_info.json', 'r') as file:
            objects = json.loads(file.read())
        return objects

    def get_image(self, id):
        return File(open(f'data/posters/serials/serial_{id}.jpeg', 'rb'))