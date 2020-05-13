from rest_framework import permissions
from rest_framework import generics
from rest_framework.generics import RetrieveAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import (
    LoginSerializer, RegisterSerializer, UserSerializer, TokenSerializer)


class LoginView(generics.GenericAPIView):

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.get_token()
        return Response(response.data, status.HTTP_200_OK)


class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.register()
        return Response(response.data, status.HTTP_200_OK)


class UserProfileView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserSerializer

    def get(self, request):

        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
