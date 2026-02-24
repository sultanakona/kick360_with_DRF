from django.db import models
from core.models import BaseModel
from accounts.models import User

class TrainingCategory(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class TrainingVideo(BaseModel):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(TrainingCategory, on_delete=models.CASCADE, related_name='videos')
    video_url = models.URLField(blank=True, null=True)
    video_file = models.FileField(upload_to='training/videos/', blank=True, null=True)
    score_required = models.IntegerField(default=0)
    duration_time = models.IntegerField(default=60)  # seconds
    points = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class TrainingCompletion(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='training_completions')
    training_video = models.ForeignKey(TrainingVideo, on_delete=models.CASCADE)
    score_achieved = models.IntegerField(default=0)
    points_awarded = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.name} completed {self.training_video.title}"
