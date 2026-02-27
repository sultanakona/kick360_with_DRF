from django.urls import path
from .views import GlobalStatsView, CountryStatsView, UserStatsListView, StatsLeaderboardView

urlpatterns = [
    path('global/', GlobalStatsView.as_view(), name='stats-global'),
    path('country/<str:country_name>/', CountryStatsView.as_view(), name='stats-country'),
    path('users/', UserStatsListView.as_view(), name='stats-users-filter'),
    path('leaderboard/', StatsLeaderboardView.as_view(), name='stats-leaderboard'),
]
