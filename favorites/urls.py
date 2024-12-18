from django.urls import path
from .views import FavoriteLocationAPIView, AddToFavoritesAPIView

urlpatterns = [
    path('', FavoriteLocationAPIView.as_view(), name='favorite-location'),
    path('<int:location_id>/add-favorite/', AddToFavoritesAPIView.as_view(), name='add-favorite'),
]
