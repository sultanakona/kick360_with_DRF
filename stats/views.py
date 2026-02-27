from rest_framework import generics, serializers
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import User
from accounts.serializers import UserSerializer
from core.exceptions import APIResponse
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from .services import LeaderboardService

class GlobalStatsSerializer(serializers.Serializer):
    pass

class GlobalStatsView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GlobalStatsSerializer

    def get(self, request, *args, **kwargs):
        # Aggregate global stats
        total_kicks = User.objects.aggregate(total=Sum('total_kicks'))['total'] or 0
        total_users = User.objects.count()
        
        return APIResponse(
            data={
                "total_global_kicks": total_kicks,
                "total_users": total_users
            },
            message="Global stats retrieved."
        )

class CountryStatsSerializer(serializers.Serializer):
    pass

class CountryStatsView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CountryStatsSerializer

    def get(self, request, country_name, *args, **kwargs):
        users_in_country = User.objects.filter(country__iexact=country_name)
        total_kicks = users_in_country.aggregate(total=Sum('total_kicks'))['total'] or 0
        total_users = users_in_country.count()
        
        return APIResponse(
            data={
                "country": country_name,
                "total_kicks": total_kicks,
                "total_users": total_users
            },
            message=f"Stats for {country_name} retrieved."
        )

class UserStatsListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['country', 'position']
    queryset = User.objects.filter(is_active=True).order_by('-total_kicks')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return APIResponse(data=serializer.data, message="Users stats retrieved.")

class LeaderboardPlayerSerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    name = serializers.CharField(allow_null=True)
    profile_image = serializers.URLField(allow_null=True)
    total_kicks = serializers.IntegerField()
    points = serializers.IntegerField()
    streak = serializers.IntegerField()

class LeaderboardResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    data = LeaderboardPlayerSerializer(many=True)
    message = serializers.CharField()

class StatsLeaderboardView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        parameters=[
            OpenApiParameter(name='filter', description='Filter type (everyone, germany, following)', required=False, type=str),
            OpenApiParameter(name='user_id', description='User ID for following filter', required=False, type=str),
        ],
        responses={200: LeaderboardResponseSerializer}
    )
    def get(self, request):
        filter_type = request.query_params.get('filter', 'everyone')
        user_id = request.query_params.get('user_id', None)
        
        user = request.user
        
        leaderboard_data = LeaderboardService.get_top_players(user, filter_type)
        
        response_data = [
            {
                "rank": i + 1,
                "name": player.name,
                "profile_image": player.profile_image.url if player.profile_image else None,
                "total_kicks": player.total_kicks,
                "points": player.points,
                "streak": player.streak
            }
            for i, player in enumerate(leaderboard_data)
        ]
        
        return Response({
            "success": True,
            "data": response_data,
            "message": f"Top 11 players ({filter_type.capitalize()})"
        })
