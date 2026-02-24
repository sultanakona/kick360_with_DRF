from rest_framework import serializers
from .models import User
from access_codes.models import AccessCode
from access_codes.services import ShopifyService

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'profile_image', 'country', 'position', 'access_code', 'total_kicks', 'rank', 'points', 'streak']
        read_only_fields = ['id', 'access_code', 'total_kicks', 'rank', 'points', 'streak']

class RegisterSerializer(serializers.ModelSerializer):
    access_code = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['name', 'profile_image', 'country', 'position', 'access_code']
        extra_kwargs = {
            'name': {'required': True},
            'country': {'required': True},
            'position': {'required': True},
        }

    def validate_access_code(self, value):
        if len(value) != 8:
            raise serializers.ValidationError("Access code must be exactly 8 characters long.")
            
        # 1. Check if already consumed locally
        if AccessCode.objects.filter(code=value, is_consumed=True).exists():
            raise serializers.ValidationError("Access code has already been used.")
            
        # 2. Check if already linked to a user
        if User.objects.filter(access_code=value).exists():
            raise serializers.ValidationError("Access code is already linked to an account.")
            
        # 3. Verify with Shopify
        verification = ShopifyService.verify_access_code(value)
        if not verification['is_valid']:
            raise serializers.ValidationError("Invalid access code.")
            
        return value

class LoginSerializer(serializers.Serializer):
    access_code = serializers.CharField(required=True)
    
    def validate_access_code(self, value):
        if not User.objects.filter(access_code=value, is_active=True).exists():
            raise serializers.ValidationError("No active account found with this access code.")
        return value
