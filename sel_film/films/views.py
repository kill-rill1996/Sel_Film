from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator
from django.db.models import Prefetch, Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from string import ascii_lowercase
from loguru import logger

from serials.models import Serial, Country as CountrySerial
from .models import Film, Genre, Actor, Director, Country
from .forms import Film1FindForm, Film2FindForm
from films.services.service import find_films
from films.services.index_films import read_id_from_log
from serials.models import Genre as Serial_Genre

# 31
# 1010
# 97
# 122
# 147
# 109


def index_page(request):
    read_id_from_log()
    header_films = Film.objects.all()[7:14]
    ten_films = Film.objects.all()[:6]
    ten_serials = Serial.objects.all()[:6]
    ten_anime = Serial.objects.filter(genres__title='аниме')[:6]
    ten_cartoons = Serial.objects.filter(genres__title='мультсериалы')[:6]
    recommended_films = Film.objects.filter(id__in=(31, 1010, 97, 122, 147, 109))
    logger.info('Запущена index page')
    return render(request, 'index.html', context={'ten_films': ten_films,
                                                  'ten_serials': ten_serials,
                                                  'ten_anime': ten_anime,
                                                  'ten_cartoons': ten_cartoons,
                                                  'header_films': header_films,
                                                  'recommended_films': recommended_films,
                                                  })


class FilmListView(generic.ListView):
    model = Film
    context_object_name = 'films'
    paginate_by = 6

    def get_queryset(self):
        genres = Genre.objects.only('title')
        countries = Country.objects.only('title')
        films = Film.objects.only('title_ru', 'title_en', 'year', 'image', 'plot')\
            .prefetch_related(Prefetch('genres', queryset=genres))\
            .prefetch_related(Prefetch('countries', queryset=countries))
        return films


class FilmDetailView(generic.DetailView):
    model = Film
    context_object_name = 'film'
    template_name = 'details.html'

    def get_object(self, queryset=None):
        genres = Genre.objects.only('title')
        actors = Actor.objects.only('first_name', 'last_name')
        directors = Director.objects.only('first_name', 'last_name')
        countries = Country.objects.only('title')
        film = Film.objects.filter(id=self.kwargs['pk']).prefetch_related(Prefetch('genres', queryset=genres))\
            .prefetch_related(Prefetch('actors', queryset=actors))\
            .prefetch_related(Prefetch('directors', queryset=directors))\
            .prefetch_related(Prefetch('countries', queryset=countries))[0]
        return film

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['rec_films'] = Film.objects.filter(genres__in=self.object.genres.all()).exclude(id=self.object.id)[:6]
        return data


def search_films(request):
    if request.method == 'POST':
        context = {}
        form_1 = Film1FindForm(request.POST)
        form_2 = Film2FindForm(request.POST)
        film_1 = None
        film_2 = None
        logger.info('Сделан запрос на подборку для фильмов')

        if form_1.is_valid():
            try:
                film_1 = Film.objects.only('title_ru', 'image', 'year').\
                    filter(title_ru__iexact=form_1.cleaned_data['film_1_title_ru'])[0]

                context['film_1'] = film_1
                logger.info(f'Искали фильм 1: {film_1}')

            except IndexError:
                context['films_1_query'] = Film.objects.only('title_ru', 'image', 'year')\
                    .filter(title_ru__icontains=form_1.cleaned_data['film_1_title_ru']).order_by('-rating')[:5]
                # log
                logger.info(f'Не удалось найти фильм 1: \"{form_1.cleaned_data["film_1_title_ru"]}\", но подобран queryset {[f"{film.id}. {film.title_ru}" for film in context["films_1_query"]]}')
                if not context['films_1_query']:
                    logger.warning(f'Не найден фильм и queryset по запросу фильма 1: \"{form_1.cleaned_data["film_1_title_ru"]}\"')

        if form_2.is_valid():
            try:
                film_2 = Film.objects.only('title_ru', 'image', 'year')\
                    .filter(title_ru__iexact=form_2.cleaned_data['film_2_title_ru'])[0]

                context['film_2'] = film_2
                logger.info(f'Искали фильм 2: {film_2}')

            except IndexError:
                context['films_2_query'] = Film.objects.only('title_ru', 'image', 'year')\
                    .filter(title_ru__icontains=form_2.cleaned_data['film_2_title_ru']).order_by('-rating')[:5]
                # log
                logger.info(f'Не удалось найти фильм 2: \"{form_2.cleaned_data["film_2_title_ru"]}\", но подобран queryset {[f"{film.id}. {film.title_ru}" for film in context["films_2_query"]]}')
                if not context['films_2_query']:
                    logger.warning(f'Не найден фильм и queryset по запросу фильма 2: \"{form_2.cleaned_data["film_2_title_ru"]}\"')

        if film_1 and film_2 and film_1 == film_2:
            context['films_duplicate'] = True
            logger.info(f'Введены одиннаковые фильмы: "{film_1}" и "{film_2}"')

        elif film_1 and film_2:
            top_ten_points = find_films(id_1=film_1.id, id_2=film_2.id)
            context['top_ten'] = Film.objects.only('title_ru', 'year', 'image')\
                .filter(id__in=[id for id, _ in top_ten_points])
            logger.info('Подборка сделана')

        context['form_1'] = form_1
        context['form_2'] = form_2

        return render(request, 'films/search_films.html', context)

    else:
        form_1 = Film1FindForm()
        form_2 = Film2FindForm()
        return render(request, 'films/search_films.html', context={
                                                                    'form_1': form_1,
                                                                    'form_2': form_2,
                                                                   })


def search(request):
    if request.method == "POST":
        context = {}
        search_data = request.POST['search_data']
        search_data_lower = request.POST['search_data'].lower()
        model_type = request.POST['currency']

        # Films
        if model_type == 'Films':
            logger.info(f'Через поиск искали фильм \"{search_data}\"')
            try:
                # Eng title
                if search_data_lower[0] in ascii_lowercase:
                    films_list = Film.objects.only('title_ru', 'title_en', 'year', 'plot', 'image')\
                        .filter(title_en__icontains=search_data_lower)\
                        .prefetch_related('genres')\
                        .prefetch_related('countries').order_by('-rating')[:20]
                    # log
                    if films_list:
                        logger.info(f'Найден список фильмов (англ. запрос): {[f"{film.id}. {film.title_ru}" for film in films_list]}')
                    else:
                        logger.warning(f'Фильмы по запросу: \"{search_data}\" не найдены {films_list}')
                else:
                    # Rus title
                    films_list = Film.objects.only('title_ru', 'title_en', 'year', 'plot', 'image')\
                        .filter(title_ru__icontains=search_data_lower)\
                        .prefetch_related('genres',)\
                        .prefetch_related('countries').order_by('-rating')[:20]
                    # log
                    if films_list:
                        logger.info(f'Найден список фильмов (рус. запрос): {[f"{film.id}. {film.title_ru}" for film in films_list]}')
                    else:
                        logger.warning(f'Фильмы по запросу: \"{search_data}\" не найдены {films_list}')

            except IndexError:
                films_list = []
                logger.warning(f'Сраблотала IndexError при поиске фильмов')
        else:
            # Serials
            logger.info(f'Через поиск искали сериал \"{search_data}\"')
            try:
                # Eng title
                if search_data_lower[0] in ascii_lowercase:
                    films_list = Serial.objects.only('title_ru', 'title_en', 'start_year', 'end_year', 'plot', 'image', 'end_status')\
                        .filter(title_en__icontains=search_data_lower)\
                        .prefetch_related('genres')\
                        .prefetch_related('countries').order_by('-rating')[:20]
                    # log
                    if films_list:
                        logger.info(f'Найден список сериалов (англ. запрос): {[f"{film.id}. {film.title_ru}" for film in films_list]}')
                    else:
                        logger.warning(f'Сериалы по запросу: \"{search_data}\" не найдены {films_list}')
                # Rus title
                else:
                    films_list = Serial.objects.only('title_ru', 'title_en', 'start_year', 'end_year', 'plot', 'image', 'end_status')\
                        .filter(title_ru__icontains=search_data_lower)\
                        .prefetch_related(Prefetch('genres', queryset=Serial_Genre.objects.all()))\
                        .prefetch_related(Prefetch('countries', queryset=CountrySerial.objects.all())).order_by('-rating')[:20]
                    # log
                    if films_list:
                        logger.info(f'Найден список сериалов (русс. запрос): {[f"{film.id}. {film.title_ru}" for film in films_list]}')
                    else:
                        logger.warning(f'Сериалы по запросу: \"{search_data}\" не найдены {films_list}')

            except IndexError:
                films_list = []
                logger.warning(f'Сраблотала IndexError при поиске сериалов')

        context['films'] = films_list
        context['search_data'] = search_data
        return render(request, 'search_results.html', context)
    else:
        return render(request, 'search_results.html')


def contact_page(request):
    if request.method == 'POST':
        message_name = request.POST.get('name', '')
        message_email = request.POST.get('email', '')
        message_subject = request.POST.get('subject', '')
        message_text = request.POST.get('message', '')
        if message_text and message_email and message_name and message_subject:
            try:
                send_mail(
                    message_name,
                    message_subject + '\n' + message_text + f'\n\nMessage from: {message_email}',
                    message_email,
                    ['w3qxnkst1ck@gmail.com', 'hizenberg228@mail.ru', '1996sasha2507@mail.ru']
                )
                logger.info(f'Отправлено сообщение от {message_name} {message_email} на тему {message_subject} \"{message_text}\" ')
                return render(request, 'contacts.html', {'message_name': message_name})
            except BadHeaderError:
                logger.error(f'Сообщение от {message_name} {message_email} на тему {message_subject} \"{message_text}\" не отправлено BadHeaderError')
                return HttpResponse('Invalid header found.')
    else:
        return render(request, 'contacts.html')


def about_page(request):
    return render(request, 'faq.html')


class FilmListView(generic.ListView):
    model = Film
    context_object_name = 'films'
    paginate_by = 8
    template_name = 'film_list.html'
    ordering = ['id']

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['genres'] = Genre.objects.all().order_by('title')
        data['countries'] = Country.objects.all().order_by('title')
        data['recommended_films'] = Film.objects.filter(id__in=(31, 1010, 97, 122, 147, 109))
        return data


class FilterFilmListView(generic.ListView):
    model = Film
    context_object_name = 'films'
    template_name = 'film_list.html'
    paginate_by = 8
    ordering = ['id']

    def get_queryset(self):
        films = Film.objects.all()
        if self.request.session.get('genre'):
            genre = self.request.session['genre'].lower()
            films = films.filter(genres__title=genre)
        if self.request.session.get('country'):
            country = self.request.session['country']
            films = films.filter(countries__title=country)
        if self.request.session.get('imbd_start'):
            print(f'imbd_start {self.request.session["imbd_start"]}')
        if self.request.session.get('imbd_end'):
            print(f'imbd_end {self.request.session["imbd_end"]}')
        if self.request.session.get('years_start'):
            years_start = self.request.session['years_start']
            years_end = self.request.session['years_end']
            films = films.filter(year__gte=years_start, year__lte=years_end)
        return films

    def post(self, *args, **kwargs):
        print(self.request.POST)
        self.request.session['genre'] = self.request.POST.get('genre')
        self.request.session['country'] = self.request.POST.get('country')

        imbd_start = self.request.POST.get('imbd_start')
        imbd_end = self.request.POST.get('imbd_end')
        if imbd_start == '0.1' and imbd_end == '9.9':
            try:
                del self.request.session['imbd_start']
                del self.request.session['imbd_end']
            except KeyError:
                pass
        else:
            self.request.session['imbd_start'] = imbd_start
            self.request.session['imbd_end'] = imbd_end

        years_start = self.request.POST.get('years_start')
        years_end = self.request.POST.get('years_end')
        if years_start == '1950' and years_end == '2021':
            try:
                del self.request.session['years_start']
                del self.request.session['years_end']
            except KeyError:
                pass
        else:
            self.request.session['years_start'] = years_start
            self.request.session['years_end'] = years_end

        films = self.get_queryset()
        paginator = Paginator(films, 8)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(self.request, 'film_list.html', {'page_obj': page_obj, 'films': page_obj})

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['genres'] = Genre.objects.all().order_by('title')
        data['countries'] = Country.objects.all().order_by('title')
        data['recommended_films'] = Film.objects.filter(id__in=(31, 1010, 97, 122, 147, 109))
        return data


class FilterSearchListView(generic.ListView):
    paginate_by = 8
    template_name = 'film_list.html'
    context_object_name = 'films'

    def get_queryset(self):
        if self.request.GET.get('years_start') == '1950' and self.request.GET.get('years_end') == '2021':
            films = Film.objects.all()
        else:
            films = Film.objects.filter(
                Q(year__gte=int(self.request.GET.get('years_start'))) &
                Q(year__lte=int(self.request.GET.get('years_end'))))

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
        context['chosen_years_start'] = self.request.GET.get('years_start')
        context['chosen_years_end'] = self.request.GET.get('years_end')

        context['genres'] = Genre.objects.all().order_by('title')
        context['countries'] = Country.objects.all().order_by('title')
        context['recommended_films'] = Film.objects.filter(id__in=(31, 1010, 97, 122, 147, 109))
        return context
