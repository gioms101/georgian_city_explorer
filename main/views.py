from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from .models import Location, Comment, Rating
from .serializers import ListLocationSerializer, DetailLocationSerializer, CreateCommentSerializer, \
    UpdateCommentSerializer, RatingSerializer, AddLikeSerializer, ReplyToCommentSerializer, IntegrateAISerializer
from .permissions import IsOwner
from .filtersets import LocationFilter
from .paginations import CustomLocationPagination
from .using_ai import TravelMap


# Create your views here.


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Location.objects.select_related('category').prefetch_related('comments', 'ratings', 'comments__user')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = LocationFilter
    search_fields = ('name',)
    pagination_class = CustomLocationPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return ListLocationSerializer
        elif self.action == 'retrieve':
            return DetailLocationSerializer
        elif self.action == 'write_comment':
            return CreateCommentSerializer
        elif self.action == 'add_rating':
            return RatingSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if request.user.is_authenticated and request.user not in instance.views.all():
            instance.views.add(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def write_comment(self, request, pk=None):
        serializer = CreateCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, location_id=pk)
        return Response({'message': "Comment Created Successfully!"}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_rating(self, request, pk=None):
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating = Rating.objects.filter(user=request.user, location_id=pk)
        if rating.exists():
            rating = rating.first()
            if rating.value == serializer.validated_data['value']:
                rating.delete()
                return Response({'message': "rating point deleted successfully!"}, status=status.HTTP_200_OK)
            else:
                rating.value = serializer.validated_data['value']
                rating.save(update_fields=['value'])
            return Response({'message': "rating point changed successfully!"}, status=status.HTTP_200_OK)
        else:
            serializer.save(user=request.user, location_id=pk)
            return Response({'message': "rating point created successfully!"}, status=status.HTTP_201_CREATED)


class CommentViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def get_serializer_class(self):
        if self.action == 'reply_to_comment':
            return ReplyToCommentSerializer
        elif self.action == 'add_like':
            return AddLikeSerializer
        return UpdateCommentSerializer

    @action(detail=True, methods=['put'], permission_classes=[IsAuthenticated])
    def reply_to_comment(self, request, pk=None):
        serializer = ReplyToCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, parent_comment_id=pk)
        return Response({'message': "Reply to comment created Successfully!"}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put'], permission_classes=[IsAuthenticated])
    def add_like(self, request, pk=None):
        comment = get_object_or_404(Comment, id=pk)
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
            return Response({"message": "Like removed."}, status=status.HTTP_200_OK)
        else:
            comment.likes.add(request.user)
            return Response({"message": "Comment liked."}, status=status.HTTP_201_CREATED)


class PopularLocationAPIView(APIView):
    serializer_class = None

    def get(self, request, *args, **kwargs):
        cached_response = cache.get('popular_locations')
        if cached_response:
            return Response(cached_response, status=status.HTTP_200_OK)
        return Response({'message': "There are no popular locations yet!"}, status=status.HTTP_200_OK)


class IntegrateAIAPIView(APIView):
    serializer_class = IntegrateAISerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = IntegrateAISerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        places = {}
        locations = Location.objects.filter(city__name=serializer.validated_data['city']).order_by('?')
        for location in locations:
            if location.category_id not in places:
                places[location.category_id] = location.name
        places = list(places.values())
        language = serializer.validated_data['language']
        ai = TravelMap()
        response = ai.create_journey_map(serializer.validated_data['city'], places, language)
        # result = response.journey_map.replace("\n", "")
        return Response(response)

