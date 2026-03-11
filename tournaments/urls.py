from django.urls import path
from .views import TournamentListView, TournamentDetailView, TournamentJoinView, TournamentLeaderboardView

urlpatterns = [
    path('', TournamentListView.as_view(), name='tournament-list'),
    path('<uuid:id>/', TournamentDetailView.as_view(), name='tournament-detail'),
    path('<uuid:id>/join/', TournamentJoinView.as_view(), name='tournament-join'),
    path('<uuid:id>/leaderboard/', TournamentLeaderboardView.as_view(), name='tournament-leaderboard'),
]
