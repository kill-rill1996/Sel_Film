from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic


from .models import Film, Actor, Director, Country, Genre
from .forms import Film1FindForm, Film2FindForm
from .service import find_films


def index_page(request):
    return render(request, 'films/index.html')


class FilmListView(generic.ListView):
    model = Film
    context_object_name = 'films'
    paginate_by = 6

    def get_queryset(self):
        return Film.objects.all().order_by('-rating')


class FilmDetailView(generic.DetailView):
    model = Film
    context_object_name = 'film'

    def get_context_data(self, **kwargs):
        film = Film.objects.get(id=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['actors'] = ', '.join([a.first_name + ' ' + a.last_name for a in film.actors.all()[:5]])
        context['countries'] = ', '.join([c.title for c in film.countries.all()])
        context['directors'] = ', '.join([d.first_name + ' ' + d.last_name for d in film.directors.all()[:5]])
        context['genres'] = ', '.join([g.title for g in film.genres.all()])
        return context


def search_films(request):

    if request.method == 'POST':
        context = {}
        form_1 = Film1FindForm(request.POST)
        form_2 = Film2FindForm(request.POST)
        film_1 = None
        film_2 = None

        if form_1.is_valid():
            try:
                film_1 = Film.objects.get(title_ru__iexact=form_1.cleaned_data['film_1_title_ru'])
                context['film_1'] = film_1
            except Film.DoesNotExist:
                context['films_1_query'] = Film.objects.filter(title_ru__icontains=form_1.cleaned_data['film_1_title_ru'])[:5]

        if form_2.is_valid():
            try:
                film_2 = Film.objects.get(title_ru__iexact=form_2.cleaned_data['film_2_title_ru'])
                context['film_2'] = film_2
            except Film.DoesNotExist:
                context['films_2_query'] = Film.objects.filter(title_ru__icontains=form_2.cleaned_data['film_2_title_ru'])[:5]
        if film_1 == film_2:
            context['films_duplicate'] = True
        elif film_1 and film_2:
            top_ten_points = find_films(id_1=film_1.id, id_2=film_2.id)
            context['top_ten'] = [Film.objects.get(id=id) for id, _ in top_ten_points]

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


def get_top_ten_films(films_points):
    top_ten_films = []
    for id, points in films_points:
        top_ten_films.append(Film.objects.get(id=id))
    return top_ten_films
