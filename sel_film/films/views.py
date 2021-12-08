from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic


from .models import Film, Actor, Director, Country, Genre
from .forms import FilmFindForm
from .service import find_films


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
        return Film.objects.all().order_by('rating')


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
        form = FilmFindForm(request.POST)

        if form.is_valid():
            try:
                film_1 = Film.objects.get(title_ru__iexact=form.cleaned_data['film_1_title_ru'])
                film_2 = Film.objects.get(title_ru__iexact=form.cleaned_data['film_2_title_ru'])
                top_ten = find_films(id_1=film_1.id, id_2=film_2.id)
                context['top_ten'] = top_ten
                context['film_1'] = film_1
                context['film_2'] = film_2

            except Film.DoesNotExist:
                context['films_1_query'] = Film.objects.filter(title_ru__icontains=form.cleaned_data['film_1_title_ru'])[:5]
                context['films_2_query'] = Film.objects.filter(title_ru__icontains=form.cleaned_data['film_2_title_ru'])[:5]

            context['form'] = form
        return render(request, 'films/search_films.html', context)

    else:
        form = FilmFindForm()
        return render(request, 'films/search_films.html', context={'form': form})
