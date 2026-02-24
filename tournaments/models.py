from django.db import models
from core.models import BaseModel
from accounts.models import User

class Tournament(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    duration_days = models.IntegerField(default=7)
    rules = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class TournamentParticipation(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tournament_participations')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='participations')
    total_kicks = models.IntegerField(default=0)
    hours_played = models.FloatField(default=0.0)
    rank = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'tournament')
        indexes = [
            models.Index(fields=['-total_kicks']),
        ]

    def __str__(self):
        return f"{self.user.name} in {self.tournament.title}"
