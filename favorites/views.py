from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Favorite
from .serializers import ListFavoriteSerializer, AddToFavoriteSerializer, ListAnonFavoriteSerializer
from main.models import Location
import ast


# Create your views here.

class FavoriteLocationAPIView(ListAPIView):
    serializer_class = ListFavoriteSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Favorite.objects.prefetch_related('location').filter(user=self.request.user)
        favorite_locations = self.request.COOKIES.get('favorite_locations')
        if favorite_locations:
            return Location.objects.filter(id__in=ast.literal_eval(favorite_locations))
        else:
            return Location.objects.none()

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return ListFavoriteSerializer
        return ListAnonFavoriteSerializer


class AddToFavoritesAPIView(APIView):
    serializer_class = AddToFavoriteSerializer

    def post(self, request, *args, **kwargs):
        location_id = kwargs.get('location_id')

        if request.user.is_authenticated:
            obj, created = Favorite.objects.get_or_create(user=request.user, location_id=location_id)
            if created:
                return Response({'message': "Location added successfully to favorites list!"},
                                status=status.HTTP_201_CREATED)
            else:
                obj.delete()
                return Response({'message': "Location removed successfully from favorites list!"},
                                status=status.HTTP_200_OK)

        fav_locs = request.COOKIES.get('favorite_locations', '[]')

        # Converting string 'fav_locs' into List using ast.literal_eval() method.
        fav_locs = ast.literal_eval(fav_locs)
        if location_id in fav_locs:
            fav_locs.remove(location_id)
            response = Response({'message': "Location removed successfully from favorites list!"},
                                status=status.HTTP_200_OK)
            response.set_cookie('favorite_locations', str(fav_locs), max_age=60)
            return response
        else:
            fav_locs.append(location_id)
            response = Response({'message': "Location added successfully to favorites list!"},
                                status=status.HTTP_201_CREATED)
            response.set_cookie('favorite_locations', str(fav_locs), max_age=60)
            return response
