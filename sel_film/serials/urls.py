from django.urls import path, include

from .views import SerialListView, search_serials

urlpatterns = [
    path('', SerialListView.as_view(), name='serial-list'),
    path('search_serials/', search_serials, name='search-serials'),
]
