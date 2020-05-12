from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import (
    LoginSerializer, RegisterSerializer, UserSerializer, TokenSerializer)

from django.contrib.auth import get_user_model
from .utils import create_auth_token

UserModel = get_user_model()


class LoginView(generics.GenericAPIView):
    permissions_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            token = create_auth_token(serializer.validated_data['user'])
            return Response({'token': token}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    model = UserModel

    def create(self, request, *args, **kwargs):  # <- here i forgot self
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        token = create_auth_token(user=serializer.instance)
        return Response({'token': token}, status=status.HTTP_201_CREATED)


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
