from rest_framework import serializers
from api.models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email',  'password']
    
    def create(self, validated_data):
        validated_data['is_active'] = False
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)