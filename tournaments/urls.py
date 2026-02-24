from django.urls import path
from .views import TournamentListView, TournamentDetailView, TournamentJoinView, TournamentLeaderboardView

urlpatterns = [
    path('', TournamentListView.as_view(), name='tournament-list'),
    path('<int:pk>/', TournamentDetailView.as_view(), name='tournament-detail'),
    path('<int:pk>/join/', TournamentJoinView.as_view(), name='tournament-join'),
    path('<int:pk>/leaderboard/', TournamentLeaderboardView.as_view(), name='tournament-leaderboard'),
]
