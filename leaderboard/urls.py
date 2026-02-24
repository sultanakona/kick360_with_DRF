from django.urls import path
from .views import GlobalLeaderboardView
from tournaments.views import TournamentLeaderboardView

urlpatterns = [
    path('global/', GlobalLeaderboardView.as_view(), name='global-leaderboard'),
    path('tournament/<int:pk>/', TournamentLeaderboardView.as_view(), name='tournament-leaderboard-redirect'),
]
