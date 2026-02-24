from rest_framework import serializers
from .models import Session

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'user', 'total_kick', 'video_file', 'mode', 'is_story', 'is_shared_to_leaderboard', 'session_duration', 'countdown_time', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

class SessionCompleteSerializer(serializers.Serializer):
    total_kick = serializers.IntegerField(required=True, min_value=0)
    video_file = serializers.FileField(required=False, allow_empty_file=False)
    mode = serializers.ChoiceField(choices=Session.MODE_CHOICES, default='default')
    is_story = serializers.BooleanField(default=False)
    is_shared_to_leaderboard = serializers.BooleanField(default=False)
    session_duration = serializers.IntegerField(default=5)
    countdown_time = serializers.IntegerField(default=3)

class SessionShareToggleSerializer(serializers.Serializer):
    share_type = serializers.ChoiceField(choices=['leaderboard', 'story'])
    state = serializers.BooleanField(required=True)
