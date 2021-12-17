from loguru import logger

from django.db.models import Prefetch
from django.shortcuts import render
from django.views import generic

from .models import Serial, Genre, Actor, Director, Country
from films.forms import Film1FindForm, Film2FindForm
from .service import find_serials


class SerialListView(generic.ListView):
    model = Serial
    context_object_name = 'films'
    paginate_by = 6

    def get_queryset(self):
        genres = Genre.objects.only('title')
        countries = Country.objects.only('title')
        return Serial.objects.only('title_ru', 'title_en', 'image', 'plot', 'start_year', 'end_year')\
            .prefetch_related(Prefetch('genres', queryset=genres))\
            .prefetch_related(Prefetch('countries', queryset=countries))


class SerialDetailView(generic.DetailView):
    model = Serial
    context_object_name = 'film'

    def get_object(self, queryset=None):
        genres = Genre.objects.only('title')
        actors = Actor.objects.only('first_name', 'last_name')
        directors = Director.objects.only('first_name', 'last_name')
        countries = Country.objects.only('title')
        serial = Serial.objects.filter(id=self.kwargs['pk']).prefetch_related(Prefetch('genres', queryset=genres))\
            .prefetch_related(Prefetch('actors', queryset=actors))\
            .prefetch_related(Prefetch('directors', queryset=directors))\
            .prefetch_related(Prefetch('countries', queryset=countries))[0]
        return serial


def search_serials(request):

    if request.method == 'POST':
        context = {}
        form_1 = Film1FindForm(request.POST)
        form_2 = Film2FindForm(request.POST)
        film_1 = None
        film_2 = None
        logger.info(f'Сделан запрос на подборку сериалов')

        if form_1.is_valid():
            try:
                film_1 = Serial.objects.only('title_ru', 'image', 'start_year', 'end_year').filter(title_ru__iexact=form_1.cleaned_data['film_1_title_ru'])[0]
                context['film_1'] = film_1
                logger.info(f'Искали сериал 1: {film_1}')

            except IndexError:
                context['films_1_query'] = Serial.objects.only('title_ru', 'image', 'start_year', 'end_year').filter(title_ru__icontains=form_1.cleaned_data['film_1_title_ru']).order_by('-rating')[:5]
                logger.info(f'Не удалось найти сериал 1: \"{form_1.cleaned_data["film_1_title_ru"]}\", но подобран queryset {[f"{film.id}. {film.title_ru}" for film in context["films_1_query"]]}')
                if not context['films_1_query']:
                    logger.warning(f'Не найдет сериал и queryset по запросу сериала 1: \"{form_1.cleaned_data["film_1_title_ru"]}\"')


        if form_2.is_valid():
            try:
                film_2 = Serial.objects.only('title_ru', 'image', 'start_year', 'end_year').filter(title_ru__iexact=form_2.cleaned_data['film_2_title_ru'])[0]
                context['film_2'] = film_2
                logger.info(f'Искали сериал 2: {film_2}')

            except IndexError:
                context['films_2_query'] = Serial.objects.only('title_ru', 'image', 'start_year', 'end_year').filter(title_ru__icontains=form_2.cleaned_data['film_2_title_ru']).order_by('-rating')[:5]
                logger.info(f'Не удалось найти сериал 2: \"{form_2.cleaned_data["film_2_title_ru"]}\", но подобран queryset {[f"{film.id}. {film.title_ru}" for film in context["films_2_query"]]}')
                if not context['films_2_query']:
                    logger.warning(f'Не найдет сериал и queryset по запросу сериала 2: \"{form_2.cleaned_data["film_2_title_ru"]}\"')

        if film_1 and film_2 and film_1 == film_2:
            context['films_duplicate'] = True
            logger.info(f'Введены одиннаковые сериалы: "{film_1}" и "{film_2}"')

        elif film_1 and film_2:
            top_ten_points = find_serials(id_1=film_1.id, id_2=film_2.id)
            context['top_ten'] = Serial.objects.only('title_ru', 'image', 'start_year', 'end_year')\
                .filter(id__in=[id for id, _ in top_ten_points])
            logger.info('Подборка сделана')

        context['form_1'] = form_1
        context['form_2'] = form_2
        return render(request, 'serials/search_serials.html', context)

    else:
        form_1 = Film1FindForm()
        form_2 = Film2FindForm()
        return render(request, 'serials/search_serials.html', context={'form_1': form_1, 'form_2': form_2})

