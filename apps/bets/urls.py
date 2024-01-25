from django.urls import include, path
from .views import BetHistoryViewSet
from rest_framework.routers import DefaultRouter

urlpatterns = [
]

router = DefaultRouter()

router.register("bets-history", BetHistoryViewSet)

urlpatterns += router.urls