from django.shortcuts import render
from django.views import generic

from .models import Serial
from films.forms import Film1FindForm, Film2FindForm
from .service import find_serials


class SerialListView(generic.ListView):
    model = Serial
    context_object_name = 'films'
    paginate_by = 6

    def get_queryset(self):
        return Serial.objects.all().order_by('-rating')


class SerialDetailView(generic.DetailView):
    model = Serial
    context_object_name = 'film'

    def get_context_data(self, **kwargs):
        serial = Serial.objects.get(id=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['actors'] = ', '.join([a.first_name + ' ' + a.last_name for a in serial.actors.all()[:5]])
        context['countries'] = ', '.join([c.title for c in serial.countries.all()])
        context['directors'] = ', '.join([d.first_name + ' ' + d.last_name for d in serial.directors.all()[:5]])
        context['genres'] = ', '.join([g.title for g in serial.genres.all()])
        return context


def search_serials(request):

    if request.method == 'POST':
        context = {}
        form_1 = Film1FindForm(request.POST)
        form_2 = Film2FindForm(request.POST)
        film_1 = None
        film_2 = None

        if form_1.is_valid():
            try:
                film_1 = Serial.objects.get(title_ru__iexact=form_1.cleaned_data['film_1_title_ru'])
                context['film_1'] = film_1
            except Serial.DoesNotExist:
                context['films_1_query'] = Serial.objects.filter(title_ru__icontains=form_1.cleaned_data['film_1_title_ru'])[:5]

        if form_2.is_valid():
            try:
                film_2 = Serial.objects.get(title_ru__iexact=form_2.cleaned_data['film_2_title_ru'])
                context['film_2'] = film_2
            except Serial.DoesNotExist:
                context['films_2_query'] = Serial.objects.filter(title_ru__icontains=form_2.cleaned_data['film_2_title_ru'])[:5]
        if film_1 and film_2:
            top_ten_points = find_serials(id_1=film_1.id, id_2=film_2.id)
            context['top_ten'] = [Serial.objects.get(id=id) for id, _ in top_ten_points]

        context['form_1'] = form_1
        context['form_2'] = form_2
        return render(request, 'serials/search_serials.html', context)

    else:
        form_1 = Film1FindForm()
        form_2 = Film2FindForm()
        return render(request, 'serials/search_serials.html', context={'form_1': form_1, 'form_2': form_2})

