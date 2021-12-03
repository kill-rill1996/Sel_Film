from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Film, Actor, Director, Country, Genre
from .forms import FilmForm

from django.views import generic


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
    paginate_by = 10

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
