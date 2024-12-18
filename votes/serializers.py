from rest_framework import serializers
from .models import PossibleLocation


class PossibleLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PossibleLocation
        fields = ('name', 'category', 'image')


class VoteToLocationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)

    class Meta:
        model = PossibleLocation
        fields = ('id',)
