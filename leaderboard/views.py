from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from accounts.models import User
from accounts.serializers import UserSerializer
from core.exceptions import APIResponse
from django.db.models import F, Window
from django.db.models.functions import Rank

class GlobalLeaderboardView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        # Annotate with a dynamic rank based on points, total_kicks, and streak
        return User.objects.filter(is_active=True).annotate(
            dynamic_rank=Window(
                expression=Rank(),
                order_by=[F('points').desc(), F('total_kicks').desc(), F('streak').desc()]
            )
        ).order_by('-points', '-total_kicks', '-streak')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        # Get top 3
        top_3 = queryset[:3]
        
        # Paginated full list
        page = self.paginate_queryset(queryset)
        
        # Current user info
        current_user = request.user
        
        response_data = {
            "top_3": self.get_serializer(top_3, many=True).data,
            "current_user": {
                "rank": getattr(current_user, 'dynamic_rank', current_user.rank),
                "total_kicks": current_user.total_kicks,
                "name": current_user.name
            },
        }

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response_data["full_list"] = self.get_paginated_response(serializer.data).data
        else:
            serializer = self.get_serializer(queryset, many=True)
            response_data["full_list"] = serializer.data

        return APIResponse(data=response_data, message="Global leaderboard retrieved.")
