from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from accounts.serializers import UserSerializer
from tournaments.models import TournamentParticipation
from core.exceptions import APIResponse

class DashboardSerializer(serializers.Serializer):
    pass

class DashboardView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DashboardSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        
        # total tournaments joined
        tournaments_count = TournamentParticipation.objects.filter(user=user).count()

        data = {
            "profile": UserSerializer(user).data,
            "total_tournaments_joined": tournaments_count
        }

        return APIResponse(data=data, message="Dashboard retrieved.")
