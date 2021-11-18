from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Film
from .forms import FilmForm

from django.views import generic


def index_page(request):
    form = FilmForm()
    if request.method == 'POST':
        form = FilmForm(request.POST)
        if form.is_valid():
            return redirect('film-detail', form.cleaned_data['id'])
    context = {'form': form}
    return render(request, 'films/index.html', context)


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
        context = super().get_context_data(**kwargs)
        context['actors_list'] = context['film'].actors.split(', ')
        context['countries_list'] = context['film'].countries.split(', ')
        context['directors_list'] = context['film'].directors.split(', ')
        context['genres_list'] = context['film'].genres.split(', ')
        return context
