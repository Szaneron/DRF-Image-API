from django.urls import include, path
from rest_framework import routers
from .views import UserImageViewSet

router = routers.DefaultRouter()
router.register(r'user-images/', UserImageViewSet, basename='user-images')

urlpatterns = [
    path('', include(router.urls))
]
