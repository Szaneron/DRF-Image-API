from django.urls import include, path
from rest_framework import routers
from .views import AccountViewSet, AccountTierViewSet

router = routers.DefaultRouter()
router.register(r'accounts/', AccountViewSet, basename='accounts')
router.register(r'tiers/', AccountTierViewSet, basename='tiers')

urlpatterns = [
    path('', include(router.urls))
]
