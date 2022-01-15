from django.urls import path
from django.views.decorators.cache import cache_page


from .views import (search_serials,
                    SerialDetailView,
                    CatalogSerialListView,)

urlpatterns = [
    path('', CatalogSerialListView.as_view(), name='serial-list'),
    path('cartoons/', CatalogSerialListView.as_view(), name='cartoon-list'),
    path('anime/', CatalogSerialListView.as_view(), name='anime-list'),
    path('search_serials/', search_serials, name='search-serials'),
    path('<int:pk>/', SerialDetailView.as_view(), name='serial-detail'),
]
