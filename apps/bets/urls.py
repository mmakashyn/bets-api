from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    BetHistoryViewSet,
    CricketMatchesView,
    SoccerMatchesView,
    BasketballMatchesView,
    GolfMatchesView,
    RugbyMatchesView,
    HockeyMatchesView,
)

urlpatterns = [
    path('cricket/', CricketMatchesView.as_view(), name='cricket_match'),
    path('soccer/', SoccerMatchesView.as_view(), name='soccer_match'),
    path('basketball/', BasketballMatchesView.as_view(), name='basketball_match'),
    path('golf/', GolfMatchesView.as_view(), name='golf_match'),
    path('rugby/', RugbyMatchesView.as_view(), name='rugby_match'),
    path('hockey/', HockeyMatchesView.as_view(), name='hockey_match'),
    path('cricket/<int:pk>/', CricketMatchesView.as_view(), name='cricket_match_details'),
    path('soccer/<int:pk>/', SoccerMatchesView.as_view(), name='soccer_match_details'),
    path('basketball/<int:pk>/', BasketballMatchesView.as_view(), name='basketball_match_details'),
    path('golf/<int:pk>/', GolfMatchesView.as_view(), name='golf_match_details'),
    path('rugby/<int:pk>/', RugbyMatchesView.as_view(), name='rugby_match_details'),
    path('hockey/<int:pk>/', HockeyMatchesView.as_view(), name='hockey_match_details'),
]

router = DefaultRouter()

router.register("bets-history", BetHistoryViewSet)

urlpatterns += router.urls
