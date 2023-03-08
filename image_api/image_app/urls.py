from django.urls import include, path
from rest_framework import routers

from .views import UploadImageView, ListImageView

router = routers.DefaultRouter()
router.register(r'upload-image/', UploadImageView, basename='upload-image')
router.register(r'list-image/', ListImageView, basename='list-image')

urlpatterns = [
    path('', include(router.urls))
]
