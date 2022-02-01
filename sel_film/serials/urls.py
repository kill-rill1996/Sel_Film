from django.urls import path
from django.views.decorators.cache import cache_page


from .views import search_serials, SerialDetailView, SerialListView, FilterSerialListView, add_review_for_serial

urlpatterns = [
    path('', cache_page(15 * 60)(SerialListView.as_view()), name='serial-list'),
    path('cartoons/', cache_page(15 * 60)(SerialListView.as_view()), name='cartoon-list'),
    path('anime/', cache_page(15 * 60)(SerialListView.as_view()), name='anime-list'),
    path('search_serials/', search_serials, name='search-serials'),
    path('<int:pk>/', SerialDetailView.as_view(), name='serial-detail'),
    path('filter_search/', FilterSerialListView.as_view(), name='filter-search-serials'),
    path('review/<int:pk>/', add_review_for_serial, name='add-serial-review'),
]
