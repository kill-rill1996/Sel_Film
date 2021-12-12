from django.urls import path
from django.views.decorators.cache import cache_page


from .views import SerialListView, search_serials, SerialDetailView

urlpatterns = [
    path('', SerialListView.as_view(), name='serial-list'),
    path('search_serials/', search_serials, name='search-serials'),
    path('<int:pk>/', SerialDetailView.as_view(), name='serial-detail'),
]
