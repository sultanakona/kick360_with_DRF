from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from access_codes.models import AccessCode
from core.exceptions import APIResponse

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()
        
        # Mark code as consumed locally
        from django.utils import timezone
        AccessCode.objects.create(
            code=user.access_code,
            is_consumed=True,
            consumed_at=timezone.now(),
            user=user
        )
        
        tokens = get_tokens_for_user(user)
        return APIResponse(
            data={
                "user": UserSerializer(user).data,
                "tokens": tokens
            },
            message="User registered successfully."
        )

class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        access_code = serializer.validated_data['access_code']
        user = User.objects.get(access_code=access_code)
        
        tokens = get_tokens_for_user(user)
        return APIResponse(
            data={
                "user": UserSerializer(user).data,
                "tokens": tokens
            },
            message="Login successful."
        )

class LogoutSerializer(serializers.Serializer):
    pass

class LogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        return APIResponse(message="Logout successful.")

