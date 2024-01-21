from django.urls import path
from .views import RegisterUser
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='obtain_token'),
    path('refresh/token/', TokenRefreshView.as_view(), name='refresh_token'),
    # path('verify/token/', TokenVerifyView.as_view(), name='verify_token'),
    path('register/user/', RegisterUser.as_view(), name='register')
]

