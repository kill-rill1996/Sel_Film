from django.conf.urls.static import static
from django.urls import path, include

from django.conf import settings
from .views import index_page, FilmListView, FilmDetailView, search_films,search


urlpatterns = [
    path('', index_page, name='index-page'),
    path('films/', FilmListView.as_view(), name='film-list'),
    path('films/<int:pk>/', FilmDetailView.as_view(), name='film-detail'),
    path('films/search_films/', search_films, name='search-films'),
    path('search/', search, name='search'),


]


