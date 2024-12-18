from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .serializers import PossibleLocationSerializer, VoteToLocationSerializer
from .models import PossibleLocation


# Create your views here.

class PossibleLocationViewSet(mixins.ListModelMixin,
                              GenericViewSet):
    queryset = PossibleLocation.objects.select_related('category').all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return PossibleLocationSerializer
        elif self.action == 'vote':
            return VoteToLocationSerializer

    @action(detail=False, methods=['patch'])
    def vote(self, request):
        serializer = VoteToLocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        location_obj = PossibleLocation.objects.get(id=serializer.validated_data['id'])
        if request.user in location_obj.votes.all():
            location_obj.votes.remove(request.user)
            return Response({'message': "Vote removed!"}, status=status.HTTP_200_OK)
        else:
            location_obj.votes.add(request.user)
            return Response({'message': "Voted successfully!"}, status=status.HTTP_200_OK)
