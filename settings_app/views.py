from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from accounts.models import User
from accounts.serializers import UserSerializer
from core.exceptions import APIResponse
from rest_framework.parsers import MultiPartParser, FormParser

class ProfileSettingsView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser) # to handle image uploads

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = True # PATCH behaviour
        instance = self.get_object()
        
        # We only want to allow updating specific fields
        allowed_fields = ['profile_image', 'country', 'position']
        
        # Filter request data to only allowed fields
        data_to_update = {k: v for k, v in request.data.items() if k in allowed_fields}
        
        serializer = self.get_serializer(instance, data=data_to_update, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return APIResponse(data=serializer.data, message="Profile updated successfully.")
