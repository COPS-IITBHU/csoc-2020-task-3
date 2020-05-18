from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import (
    LoginSerializer, RegisterSerializer, UserSerializer, TokenSerializer)


def create_auth_token(user):
    """
    Returns the token required for authentication for a user.
    """
    token, _ = Token.objects.get_or_create(user=user)
    return token


class LoginView(generics.GenericAPIView):
    """
    TODO:
    Implement login functionality, taking username and password
    as input, and returning the Token.
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username=serializer.data['username']
            password=serializer.data['password']
            user = authenticate(username=username, password=password)
            if user:
                token=create_auth_token(user)
                return Response({"token":token.key},status=status.HTTP_200_OK)
            else:
                return Response({"error":"Wrong credentials"}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(generics.CreateAPIView):
    """
    TODO:
    Implement register functionality, registering the user by
    taking his details, and returning the Token.
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = RegisterSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            token=create_auth_token(serializer.instance)
            return Response({'token':token.key}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveAPIView):
    """
    TODO:
    Implement the functionality to retrieve the details
    of the logged in user.
    """
    serializer_class = UserSerializer
    def get(self, request, *args, **kwargs):
        try:
            header=request.headers['Authorization']
        except Exception:
            return Response({
            "detail": "Authentication credentials were not provided."
            }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            token = header.split(' ')[1]
            try:
                user = Token.objects.get(key=token).user
            except Token.DoesNotExist:
                return Response({"detail":"Invalid Token"},status=status.HTTP_404_NOT_FOUND)
            else:
                serializer = self.get_serializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
