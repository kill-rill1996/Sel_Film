from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator
from django.db.models import Prefetch, Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from string import ascii_lowercase
from loguru import logger

from serials.models import Serial, Country as CountrySerial
from .models import Film, Genre, Actor, Director, Country, Comment
from .forms import Film1FindForm, Film2FindForm, ReviewForm, CommentForm, RecaptchaForm
from films.services.service import find_films
from films.services.week_films import read_id_from_log
from serials.models import Genre as Serial_Genre


def index_page(request):
    week_films = Film.objects.filter(id__in=read_id_from_log())\
                    .prefetch_related(Prefetch('genres', queryset=Genre.objects.only('title')))\
                    .only('title_ru', 'image', 'rating')
    ten_films = Film.objects.all().prefetch_related(Prefetch('genres', queryset=Genre.objects.only('title')))\
                    .only('image', 'rating', 'title_ru', 'plot', 'year')[:6]
    ten_serials = Serial.objects.all()\
                    .prefetch_related(Prefetch('genres', queryset=Serial_Genre.objects.only('title')))\
                    .only('image', 'plot', 'title_ru', 'rating', 'start_year', 'end_year')[:6]
    ten_anime = Serial.objects.filter(genres__title='аниме')\
                    .prefetch_related(Prefetch('genres', queryset=Serial_Genre.objects.only('title')))\
                    .only('image', 'plot', 'title_ru', 'rating', 'start_year', 'end_year')[:6]
    ten_cartoons = Serial.objects.filter(genres__title='мультсериалы')\
                    .prefetch_related(Prefetch('genres', queryset=Serial_Genre.objects.only('title')))\
                    .only('image', 'plot', 'title_ru', 'rating', 'start_year', 'end_year')[:6]
    recommended_films = Film.objects.filter(id__in=(31, 1010, 97, 122, 147, 109))\
                    .prefetch_related(Prefetch('genres', queryset=Genre.objects.only('title')))\
                    .only('title_ru', 'rating', 'image')
    logger.info('Запущена index page')
    return render(request, 'index.html', context={'ten_films': ten_films,
                                                  'ten_serials': ten_serials,
                                                  'ten_anime': ten_anime,
                                                  'ten_cartoons': ten_cartoons,
                                                  'week_films': week_films,
                                                  'recommended_films': recommended_films,
                                                  })


# Old film list
# class FilmListView(generic.ListView):
#     model = Film
#     context_object_name = 'films'
#     paginate_by = 6
#
#     def get_queryset(self):
#         genres = Genre.objects.only('title')
#         countries = Country.objects.only('title')
#         films = Film.objects.only('title_ru', 'title_en', 'year', 'image', 'plot')\
#             .prefetch_related(Prefetch('genres', queryset=genres))\
#             .prefetch_related(Prefetch('countries', queryset=countries))
#         return films


class FilmDetailView(generic.DetailView):
    model = Film
    context_object_name = 'film'
    template_name = 'details.html'

    def get_object(self, queryset=None):
        genres = Genre.objects.only('title')
        actors = Actor.objects.only('first_name', 'last_name')
        directors = Director.objects.only('first_name', 'last_name')
        countries = Country.objects.only('title')
        comments = Comment.objects.all().order_by('-date_pub')
        film = Film.objects.filter(id=self.kwargs['pk']).prefetch_related(Prefetch('genres', queryset=genres))\
            .prefetch_related(Prefetch('actors', queryset=actors))\
            .prefetch_related(Prefetch('directors', queryset=directors))\
            .prefetch_related(Prefetch('countries', queryset=countries))\
            .prefetch_related(Prefetch('comments', queryset=comments))[0]
        return film

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['type'] = 'film'
        data['reviews'] = Film.objects.get(id=self.kwargs['pk']).reviews.order_by('-created')
        data['rec_films'] = Film.objects.filter(genres__in=self.object.genres.all()).exclude(id=self.object.id)[:6]
        data['captcha'] = RecaptchaForm
        return data

    def post(self, *args, **kwargs):
        form = CommentForm(self.request.POST)
        film = Film.objects.get(id=self.kwargs['pk'])
        if form.is_valid() and self.request.POST.get('g-recaptcha-response'):
            form = form.save(commit=False)
            form.film = film
            if self.request.POST.get('parent', None):
                form.is_child = True
                form.parent_id = self.request.POST.get('parent')
            form.save()
        return redirect(film.get_absolute_url())


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
            context['top_ten'] = Film.objects.only('title_ru', 'year', 'image', 'rating')\
                .prefetch_related(Prefetch('genres', queryset=Genre.objects.only('title')))\
                .filter(id__in=top_ten_points)

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


def contact_page(request):
    if request.method == 'POST':
        message_name = request.POST.get('name', '')
        message_email = request.POST.get('email', '')
        message_subject = request.POST.get('subject', '')
        message_text = request.POST.get('message', '')
        if message_text and message_email and message_name and message_subject and request.POST.get('g-recaptcha-response'):
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
        captcha = RecaptchaForm
        return render(request, 'contacts.html', {'captcha': captcha})


def about_page(request):
    return render(request, 'faq.html')


class FilmListView(generic.ListView):
    model = Film
    context_object_name = 'films'
    paginate_by = 8
    template_name = 'film_list.html'
    ordering = ['id']

    def get_queryset(self):
        genres = Genre.objects.only('title')
        countries = Country.objects.only('title')

        films = Film.objects.only('title_ru', 'year', 'image', 'plot', 'rating')\
            .prefetch_related(Prefetch('genres', queryset=genres))\
            .prefetch_related(Prefetch('countries', queryset=countries))
        return films

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['genres'] = Genre.objects.only('title').order_by('title')
        data['countries'] = Country.objects.only('title').order_by('title')
        data['recommended_films'] = Film.objects.filter(id__in=(31, 1010, 97, 122, 147, 109))\
            .prefetch_related(Prefetch('genres', queryset=data['genres']))\
            .prefetch_related(Prefetch('countries', queryset=data['countries']))
        return data


class FilterFilmListView(generic.ListView):
    paginate_by = 8
    template_name = 'film_list.html'
    context_object_name = 'films'

    def get_queryset(self):
        if self.request.GET.get('years_start') == '1900' and self.request.GET.get('years_end') == '2021':
            genres = Genre.objects.only('title')
            countries = Country.objects.only('title')
            films = Film.objects.only('title_ru', 'year', 'image', 'plot', 'rating') \
                .prefetch_related(Prefetch('genres', queryset=genres)) \
                .prefetch_related(Prefetch('countries', queryset=countries))
        else:
            genres = Genre.objects.only('title')
            countries = Country.objects.only('title')
            films = Film.objects.filter(
                Q(year__gte=int(self.request.GET.get('years_start'))) &
                Q(year__lte=int(self.request.GET.get('years_end')))
            ).only('title_ru', 'year', 'image', 'plot', 'rating')\
                .prefetch_related(Prefetch('genres', queryset=genres))\
                .prefetch_related(Prefetch('countries', queryset=countries))

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

        context['genres'] = Genre.objects.only('title').order_by('title')
        context['countries'] = Country.objects.only('title').order_by('title')
        context['recommended_films'] = Film.objects.filter(id__in=(31, 1010, 97, 122, 147, 109)) \
            .prefetch_related(Prefetch('genres', queryset=context['genres'])) \
            .prefetch_related(Prefetch('countries', queryset=context['countries']))
        return context


class SearchView(generic.ListView):
    context_object_name = 'films'
    template_name = 'film_list.html'
    paginate_by = 8

    def get_queryset(self):
        if self.request.GET.get('search_text') and self.request.GET.get('search_text') != ' ':
            search_data = self.request.GET.get('search_text')
            search_data_lower = search_data.lower()
            try:
                # Eng title
                if search_data_lower[0] in ascii_lowercase:
                    films_list = Film.objects.only('title_ru', 'year', 'plot', 'image', 'rating')\
                                     .filter(title_en__icontains=search_data_lower) \
                                     .prefetch_related('genres') \
                                     .prefetch_related('countries')[:100]
                    serials_list = Serial.objects.only('title_ru', 'rating', 'start_year', 'end_year', 'plot', 'image', 'end_status')\
                                    .filter(title_en__icontains=search_data_lower)\
                                    .prefetch_related('genres')\
                                    .prefetch_related('countries')[:100]
                    if not films_list and not serials_list:
                        logger.warning(f'Фильмы и сериалы по запросу: \"{search_data}\" не найдены {films_list} {serials_list}')
                else:
                    # Rus title
                    films_list = Film.objects.only('title_ru', 'year', 'plot', 'image', 'rating') \
                                     .filter(title_ru__icontains=search_data_lower) \
                                     .prefetch_related('genres',) \
                                     .prefetch_related('countries')[:100]
                    serials_list = Serial.objects.only('title_ru', 'rating', 'start_year', 'end_year', 'plot', 'image', 'end_status') \
                                    .filter(title_ru__icontains=search_data_lower) \
                                    .prefetch_related('genres') \
                                    .prefetch_related('countries')[:100]
                    # log
                    if not films_list and not serials_list:
                        logger.warning(f'Фильмы и сериалы по запросу: \"{search_data}\" не найдены {films_list} {serials_list}')

                films_list = list(films_list) + list(serials_list)
                films_list = sorted(films_list, key=lambda f: f.id)

            except IndexError:
                films_list = []
                logger.warning(f'Сраблотала IndexError при поиске фильмов')
            return films_list
        else:
            raise Exception

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_text'] = self.request.GET.get("search_text")
        context['search_query'] = f'search_text={self.request.GET.get("search_text")}&'
        context['genres'] = Genre.objects.all().order_by('title')
        context['countries'] = Country.objects.all().order_by('title')
        context['recommended_films'] = Film.objects.filter(id__in=(31, 1010, 97, 122, 147, 109)) \
            .prefetch_related(Prefetch('genres', queryset=context['genres'])) \
            .prefetch_related(Prefetch('countries', queryset=context['countries']))
        return context


def add_review_for_film(request, pk):
    form = ReviewForm(request.POST)
    film = Film.objects.get(id=pk)
    if form.is_valid():
        form = form.save(commit=False)
        form.film = film
        form.save()
    return redirect(film.get_absolute_url())
