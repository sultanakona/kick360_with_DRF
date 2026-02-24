from django.db import models
from core.models import BaseModel
from accounts.models import User

class Follow(BaseModel):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.name} follows {self.following.name}"
