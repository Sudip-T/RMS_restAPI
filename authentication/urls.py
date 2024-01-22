from django.urls import path
from .views import (
    RegisterUserView,UserProfileView, ChangePasswordView,SendPasswordResetEmailView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='obtain_token'),
    path('refresh/token/', TokenRefreshView.as_view(), name='refresh_token'),
    # path('verify/token/', TokenVerifyView.as_view(), name='verify_token'),
    path('register/user/', RegisterUserView.as_view(), name='register'),
    path('user/profile/', UserProfileView.as_view(), name='userprofile'),
    path('password/change/', ChangePasswordView.as_view(), name='changepassword'),
    path('password/reset/email/', SendPasswordResetEmailView.as_view(), name='send-password-reset'),
]

