from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic


from .models import Film, Actor, Director, Country, Genre
from .forms import FilmForm
from .service import main


def index_page(request):
    # form = FilmForm()
    # if request.method == 'POST':
    #     form = FilmForm(request.POST)
    #     if form.is_valid():
    #         return redirect('film-detail', form.cleaned_data['id'])
    # context = {'form': form}
    return render(request, 'films/index.html')


class FilmListView(generic.ListView):
    model = Film
    context_object_name = 'films'
    paginate_by = 6

    def get_queryset(self):
        return Film.objects.all()


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
    context = {}

    if request.method == "POST":
        field_1_title = request.POST['film_1']
        field_2_title = request.POST['film_2']
        try:
            film_1 = Film.objects.get(title_ru__iexact=field_1_title)
            film_2 = Film.objects.get(title_ru__iexact=field_2_title)
            print(film_1, film_2)
            top_ten = main(film_1.id, film_2.id)
            context['top_ten'] = top_ten
            context['film_1'] = film_1
            context['film_2'] = film_2
        except:
            context['films_query_1'] = Film.objects.filter(title_ru__icontains=field_1_title)
            context['films_query_2'] = Film.objects.filter(title_ru__icontains=field_2_title)

        return render(request, 'films/search_films.html', context)

    else:
        return render(request, 'films/search_films.html', {})