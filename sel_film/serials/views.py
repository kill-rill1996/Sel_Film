from loguru import logger

from django.db.models import Prefetch, Q
from django.shortcuts import render
from django.views import generic

from films.models import Film
from .models import Serial, Genre, Actor, Director, Country
from films.forms import Film1FindForm, Film2FindForm
from .service import find_serials


class SerialListView(generic.ListView):
    model = Serial
    context_object_name = 'films'
    paginate_by = 8
    template_name = 'serial_list.html'

    def get_queryset(self):
        searched_type = get_serial_type(self.request)
        if searched_type[0]:
            return Serial.objects.filter(genres__title=searched_type[0])
        return Serial.objects.all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        serial_type = get_serial_type(self.request)
        data['list_type'] = serial_type[1]
        if serial_type[0]:
            data['list_type'] = serial_type[0]
            data['chosen_genre'] = serial_type[2]

        data['genres'] = Genre.objects.all().order_by('title')
        data['countries'] = Country.objects.all().order_by('title')
        data['recommended_films'] = Film.objects.filter(id__in=(31, 1010, 97, 122, 147, 109))
        return data


def get_serial_type(request):
    if request.path == '/serials/anime/':
        searched_type = ('аниме', 'аниме', 'Аниме')
    elif request.path == '/serials/cartoons/':
        searched_type = ('мультсериалы', 'мультфильмов', 'Мультсериалы')
    else:
        searched_type = (None, 'сериалов', None)
    return searched_type


class SerialDetailView(generic.DetailView):
    model = Serial
    context_object_name = 'film'
    template_name = 'details.html'

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

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        serial_genres = [genre.title for genre in self.object.genres.all()]
        if 'аниме' in serial_genres:
            data['rec_films'] = Serial.objects.filter(genres__title='аниме').exclude(
                id=self.object.id)[:6]
        elif 'мультсериалы' in serial_genres:
            data['rec_films'] = Serial.objects.filter(genres__title='мультсериалы').exclude(
                id=self.object.id)[:6]
        else:
            data['rec_films'] = Serial.objects.exclude(id=self.object.id)[:6]
        return data


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


class FilterSerialListView(generic.ListView):
    paginate_by = 8
    template_name = 'serial_list.html'
    context_object_name = 'films'

    def get_queryset(self):
        if self.request.GET.get('years_start') == '1900' and self.request.GET.get('years_end') == '2021':
            films = Serial.objects.all()
        else:
            films = Serial.objects.filter(
                Q(start_year__gte=int(self.request.GET.get('years_start'))) &
                Q(start_year__lte=int(self.request.GET.get('years_end')))
            )

        if self.request.GET.get('imbd_start') != '0.1' or self.request.GET.get('imbd_end') != '9.9':
            films = films.filter(
                Q(rating__gte=float(self.request.GET.get('imbd_start'))) &
                Q(rating__lte=float(self.request.GET.get('imbd_end')))
            )

        if self.request.GET.get('genre') and self.request.GET.get('genre') != 'Все жанры':
            films = films.filter(genres__title=self.request.GET.get('genre').lower())

        if self.request.GET.get('country') and self.request.GET.get('country') != 'Все страны':
            films = films.filter(countries__title=self.request.GET.get('country'))
        return films

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['get_params'] = []
        if self.request.GET.get('genre'):
            context['get_params'].append(f"genre={self.request.GET.get('genre')}&")
            context['chosen_genre'] = self.request.GET.get('genre')
        if self.request.GET.get('country'):
            context['get_params'].append(f"country={self.request.GET.get('country')}&")
            context['chosen_country'] = self.request.GET.get('country')
        context['get_params'].append(f"years_start={self.request.GET.get('years_start')}&")
        context['get_params'].append(f"years_end={self.request.GET.get('years_end')}&")
        context['get_params'].append(f"imbd_start={self.request.GET.get('imbd_start')}&")
        context['get_params'].append(f"imbd_end={self.request.GET.get('imbd_end')}&")

        context['list_type'] = 'сериалов'
        context['genres'] = Genre.objects.all().order_by('title')
        context['countries'] = Country.objects.all().order_by('title')
        context['recommended_films'] = Film.objects.filter(id__in=(31, 1010, 97, 122, 147, 109))
        return context
