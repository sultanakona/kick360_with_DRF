from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import TrainingCategory, TrainingVideo
from .serializers import TrainingCategorySerializer, TrainingVideoSerializer, CompleteTrainingRequestSerializer, TrainingCompletionSerializer
from .services import TrainingService
from core.exceptions import APIResponse
from django_filters.rest_framework import DjangoFilterBackend

class TrainingVideoListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TrainingVideoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'category__name']

    def get_queryset(self):
        return TrainingVideo.objects.filter(is_active=True).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return APIResponse(data=serializer.data, message="Training videos retrieved.")

class TrainingCompleteView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CompleteTrainingRequestSerializer

    def post(self, request, pk, *args, **kwargs):
        training_video = get_object_or_404(TrainingVideo, pk=pk, is_active=True)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        score_achieved = serializer.validated_data.get('score_achieved', 0)
        
        completion = TrainingService.complete_training(
            user=request.user,
            training_video=training_video,
            score_achieved=score_achieved
        )
        
        return APIResponse(
            data=TrainingCompletionSerializer(completion).data,
            message="Training completed successfully."
        )
