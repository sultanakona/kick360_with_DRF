from rest_framework import serializers
from .models import TrainingCategory, TrainingVideo, TrainingCompletion
from accounts.serializers import UserSerializer

class TrainingCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingCategory
        fields = ['id', 'name', 'is_active', 'created_at']

class TrainingVideoSerializer(serializers.ModelSerializer):
    category = TrainingCategorySerializer(read_only=True)
    
    class Meta:
        model = TrainingVideo
        fields = ['id', 'title', 'category', 'video_url', 'video_file', 'score_required', 'duration_time', 'points', 'is_active', 'created_at']

class TrainingCompletionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    training_video = TrainingVideoSerializer(read_only=True)

    class Meta:
        model = TrainingCompletion
        fields = ['id', 'user', 'training_video', 'score_achieved', 'points_awarded', 'created_at']

class CompleteTrainingRequestSerializer(serializers.Serializer):
    score_achieved = serializers.IntegerField(default=0)
