from django.shortcuts import render
from django.views import generic

from .models import Serial
from films.forms import FilmFindForm
from .service import find_serials

class SerialListView(generic.ListView):
    model = Serial
    context_object_name = 'serials'
    paginate_by = 6

    def get_queryset(self):
        return Serial.objects.all().order_by('rating')


def search_serials(request):

    if request.method == 'POST':
        context = {}
        form = FilmFindForm(request.POST)

        if form.is_valid():
            try:
                film_1 = Serial.objects.get(title_ru__iexact=form.cleaned_data['film_1_title_ru'])
                film_2 = Serial.objects.get(title_ru__iexact=form.cleaned_data['film_2_title_ru'])
                top_ten = find_serials(id_1=film_1.id, id_2=film_2.id)
                context['top_ten'] = top_ten
                context['film_1'] = film_1
                context['film_2'] = film_2

            except Serial.DoesNotExist:
                context['films_1_query'] = Serial.objects.filter(title_ru__icontains=form.cleaned_data['film_1_title_ru'])[:5]
                context['films_2_query'] = Serial.objects.filter(title_ru__icontains=form.cleaned_data['film_2_title_ru'])[:5]

            context['form'] = form
        return render(request, 'serials/search_serials.html', context)

    else:
        form = FilmFindForm()
        return render(request, 'serials/search_serials.html', context={'form': form})

