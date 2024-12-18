from rest_framework import serializers
from .models import Favorite


class ListFavoriteSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='location.name')
    location_city = serializers.CharField(source='location.city')
    location_address = serializers.CharField(source='location.address')
    location_image = serializers.ImageField(source='location.image')

    class Meta:
        model = Favorite
        fields = ('location_name', 'location_city', 'location_address', 'location_image')


class AddToFavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ('location_id',)
