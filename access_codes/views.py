from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .models import AccessCode
from .serializers import AccessCodeSerializer
from .services import ShopifyService
from core.exceptions import APIResponse
import logging

logger = logging.getLogger(__name__)

class AccessCodeVerifyView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AccessCodeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        code = serializer.validated_data['code']
        
        try:
            # Verify with Shopify
            result = ShopifyService.verify_access_code(code)
            
            if not result['is_valid']:
                return APIResponse(
                    data={},
                    message=result.get('meta', {}).get('error', 'Invalid access code'),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if code exists and is not consumed
            access_code, created = AccessCode.objects.get_or_create(
                code=code,
                defaults={
                    'user': request.user,
                    'is_consumed': False
                }
            )
            
            if access_code.is_consumed:
                return APIResponse(
                    data={},
                    message="This access code has already been used.",
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Consume the code
            access_code.is_consumed = True
            access_code.user = request.user
            access_code.consumed_at = timezone.now()
            access_code.save()
            
            return APIResponse(
                data=AccessCodeSerializer(access_code).data,
                message="Access code verified and consumed successfully."
            )
            
        except Exception as e:
            logger.error(f"Error verifying access code: {str(e)}")
            return APIResponse(
                data={},
                message="An error occurred while verifying the access code.",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
