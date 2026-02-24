from django.db import transaction
from .models import TrainingVideo, TrainingCompletion
from accounts.models import User

class TrainingService:
    @staticmethod
    @transaction.atomic
    def complete_training(user: User, training_video: TrainingVideo, score_achieved: int) -> TrainingCompletion:
        """
        User completes a training video, recording the score and updating user points.
        """
        # Assume score achieved needs to be somewhat recorded and verified. 
        # Even if not strict, the user gets points.
        points_to_award = training_video.points
        
        completion = TrainingCompletion.objects.create(
            user=user,
            training_video=training_video,
            score_achieved=score_achieved,
            points_awarded=points_to_award
        )
        
        user.points += points_to_award
        user.save(update_fields=['points'])
        
        return completion
