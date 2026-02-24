from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from accounts.models import User
from accounts.serializers import UserSerializer
from core.exceptions import APIResponse
from django.db.models import F

class GlobalLeaderboardView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        # Already indexed on -total_kicks
        return User.objects.filter(is_active=True).order_by('-total_kicks')

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
                "rank": current_user.rank,
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
