from django.contrib import admin
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from api.views import LoginViewSet,VerifyOTPViewSet,RegisterViewSet,CustomObtainAuthToken

# router = DefaultRouter()
# router.register('registerapi',RegisterViewSet,basename='registerapi')
# router.register('verify',VerifyOTPViewSet,basename='verify')
# router.register('login', LoginViewSet, basename='login')

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include(router.urls)),
#     path('api-token-auth/', CustomObtainAuthToken.as_view(), name='api_token_auth'),
# ]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import RegisterViewSet, VerifyOTPViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register('registerapi', RegisterViewSet, basename='register')
router.register('verify-otp', VerifyOTPViewSet, basename='verify-otp')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('accounts/', include('allauth.urls')),
    path('', include('api.urls')),
]
