from accounts.models import User

class LeaderboardService:
    @staticmethod
    def get_top_players(user, filter_type):
        """
        Return the top 11 players based on the filter type.
        """
        if filter_type == 'everyone':
            return User.objects.all().order_by('-total_kicks')[:11]
        
        elif filter_type == 'germany':
            return User.objects.filter(country__iexact='Germany').order_by('-total_kicks')[:11]
        
        elif filter_type == 'following':
            if user and hasattr(user, 'following'):
                following_user_ids = user.following.values_list('following_id', flat=True)
                return User.objects.filter(id__in=following_user_ids).order_by('-total_kicks')[:11]
            return User.objects.none()
        
        return User.objects.none()
