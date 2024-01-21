from rest_framework import status
from .serializers import UserRegisterSerializer,ChangePasswordSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from .models import CustomUser


# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }


class RegisterUserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'msg':'Registration Successful','token':token}, status=status.HTTP_201_CREATED)
    

class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserRegisterSerializer(request.user)
        return Response({'msg':'user info', 'data':serializer.data}, status=status.HTTP_200_OK)
    


# class ChangePasswordView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request, format=None):
#         serializer = ChangePasswordSerializer(data=request.data)
#         if serializer.is_valid():
#             old_password = serializer.validated_data['old_password']
#             new_password = serializer.validated_data['new_password']
#             new_password2 = serializer.validated_data['new_password2']
#             user = request.user

#             if not user.check_password(old_password):
#                 return Response({"detail": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

#             if new_password != new_password2:
#                 return Response({"detail": "New password and Confirm password don't match."}, status=status.HTTP_400_BAD_REQUEST)

#             user.set_password(new_password)
#             user.save()
#             return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ChangePasswordView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)