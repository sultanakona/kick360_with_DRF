from django.utils import timezone
from .models import Tournament, TournamentParticipation
from accounts.models import User

class TournamentService:
    @staticmethod
    def join_tournament(user: User, tournament: Tournament) -> TournamentParticipation:
        """
        User joins a tournament. Enforces "join once" rule implicitly via get_or_create 
        and unique constraint on the model.
        """
        if not tournament.is_active:
            raise ValueError("This tournament is no longer active.")
            
        participation, created = TournamentParticipation.objects.get_or_create(
            user=user,
            tournament=tournament,
            defaults={
                'total_kicks': 0,
                'hours_played': 0.0,
                'rank': 0
            }
        )
        
        if not created:
            raise ValueError("You have already joined this tournament.")
            
        return participation
        
    @staticmethod
    def recalculate_tournament_rank(tournament: Tournament):
        """
        Recalculates rank for a specific tournament based on total_kicks.
        """
        participations = TournamentParticipation.objects.filter(tournament=tournament).order_by('-total_kicks')
        for i, p in enumerate(participations):
            if p.rank != i + 1:
                p.rank = i + 1
                p.save(update_fields=['rank'])
