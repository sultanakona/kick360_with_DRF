from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from accounts.models import User
from accounts.serializers import UserSerializer
from core.exceptions import APIResponse
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum

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
