from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework.response import Response
from api.mails import send_otp_via_email
from api.models import User
from api.serializers import UserSerializer,VerifyOTPSerializer
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.authtoken.views import ObtainAuthToken

from .models import User
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from rest_framework_simplejwt.tokens import AccessToken


class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
   

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_otp_via_email(serializer.data['email'])
            return Response({
                "msg": "Registration Successfully. Check Your Email",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPViewSet(viewsets.ModelViewSet):
    queryset = User.objects.none()

    serializer_class = VerifyOTPSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            user = User.objects.filter(email=email).first()

            if not user:
                return Response({
                    "msg": "User Not Found",
                    "data": "Invalid email"
                }, status=status.HTTP_400_BAD_REQUEST)

            if user.otp != otp:
                return Response({
                    "msg": "Wrong OTP",
                    "data": "Incorrect OTP"
                }, status=status.HTTP_400_BAD_REQUEST)
                
            user.is_active = True
            user.save()

            return Response({
                "msg": "Account verified successfully",
                "data": "User verified"
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CustomObtainAuthToken(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)
#         user = Token.objects.get(key=response.data['token']).user
#         serializer = UserSerializer(user)
#         return Response({'token': response.data['token'], 'user': serializer.data})

# class LoginViewSet(viewsets.GenericViewSet):
#     serializer_class = LoginSerializer

#     @action(detail=False, methods=['post'])
#     def login(self, request):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             password = serializer.validated_data['password']
#             user = authenticate(request, email=email, password=password)

#             if user and user.is_verified:
#                 token, created = Token.objects.get_or_create(user=user)
#                 user_serializer = UserSerializer(user)
#                 return Response({'token': token.key, 'user': user_serializer.data}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'msg': 'Invalid credentials or unverified email'}, status=status.HTTP_401_UNAUTHORIZED)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def home(request):
    user = request.user
    context = {}
    if user.is_authenticated:
        context['token'] = str(AccessToken.for_user(user))
    return render(request, 'home.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('/')
