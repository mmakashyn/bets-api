from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    BetHistoryViewSet,
    CricketMatchesView,
    FootballMatchesView,
    BasketballMatchesView,
    GolfMatchesView,
    RugbyMatchesView,
)

urlpatterns = [
    path('cricket/', CricketMatchesView.as_view(), name='cricket_match'),
    path('football/', FootballMatchesView.as_view(), name='football_match'),
    path('basketball/', BasketballMatchesView.as_view(), name='basketball_match'),
    path('golf/', GolfMatchesView.as_view(), name='golf_match'),
    path('rugby/', RugbyMatchesView.as_view(), name='rugby_match'),
    path('cricket/<int:pk>/', CricketMatchesView.as_view(), name='cricket_match_details'),
    path('football/<int:pk>/', FootballMatchesView.as_view(), name='football_match_details'),
    path('basketball/<int:pk>/', BasketballMatchesView.as_view(), name='basketball_match_details'),
    path('golf/<int:pk>/', GolfMatchesView.as_view(), name='golf_match_details'),
    path('rugby/<int:pk>/', RugbyMatchesView.as_view(), name='rugby_match_details'),
]

router = DefaultRouter()

router.register("bets-history", BetHistoryViewSet)

urlpatterns += router.urls
