from django.urls import path
from django.views.decorators.cache import cache_page

from .views import index_page, FilmDetailView, search_films, contact_page, FilmListView, about_page, FilterFilmListView, \
    SearchView, add_review_for_film

urlpatterns = [
    path('', index_page, name='index-page'),
    path('contacts/', contact_page, name='contact-page'),
    path('search/', SearchView.as_view(), name='search'),
    path('about/', about_page, name='about-page'),
    path('films/', cache_page(15 * 60)(FilmListView.as_view()), name='film-list'),
    path('films/<int:pk>/', FilmDetailView.as_view(), name='film-detail'),
    path('films/search_films/', search_films, name='search-films'),
    path('films/filter_search/', FilterFilmListView.as_view(), name='filter-search-films'),
    path('films/review/<int:pk>/', add_review_for_film, name='add-film-review'),
]


