from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Favorite
from .serializers import ListFavoriteSerializer, AddToFavoriteSerializer


# Create your views here.

class FavoriteLocationAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ListFavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.prefetch_related('location').filter(user=self.request.user)


class AddToFavoritesAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddToFavoriteSerializer

    def post(self, request, *args, **kwargs):
        location_id = kwargs.get('location_id')

        obj, created = Favorite.objects.get_or_create(user=request.user, location_id=location_id)
        if created:
            return Response({'message': "Location added successfully to favorites list!"},
                            status=status.HTTP_201_CREATED)
        else:
            obj.delete()
            return Response({'message': "Location removed successfully from favorites list!"},
                            status=status.HTTP_200_OK)

