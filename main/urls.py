from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LocationViewSet, CommentViewSet, PopularLocationAPIView, IntegrateAIAPIView

router = DefaultRouter()

router.register(r'locations', LocationViewSet, basename='locations')
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('popular-locations/', PopularLocationAPIView.as_view(), name='popular-locations'),
    path('generate-journey/', IntegrateAIAPIView.as_view(), name='integrate-ai'),
]
