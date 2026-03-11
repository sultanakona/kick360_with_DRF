from django.db.models import Sum, F
from django.utils import timezone
from .models import PerformanceTrack
from accounts.models import User

class LeaderboardService:
    @staticmethod
    def get_top_players(user, filter_type):
        """
        Return the top 11 players based on the filter type.
        Sorted by total points descending.
        """
        # Base queryset: all active users
        users = User.objects.filter(is_active=True)
        
        if filter_type == 'germany':
            users = users.filter(country__iexact='Germany')
        elif filter_type == 'following' and user:
            # Get IDs of users being followed
            following_user_ids = user.following.values_list('following_id', flat=True)
            users = users.filter(id__in=following_user_ids)
            
        # Order by points descending and take top 11
        top_players = users.order_by('-points', 'name')[:11]
        
        return top_players
