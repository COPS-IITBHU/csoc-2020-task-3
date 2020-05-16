from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import (
    LoginSerializer, RegisterSerializer, UserSerializer, TokenSerializer)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


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
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
        username = validated_data['username']
        password = validated_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            return Response({
                "token": str(create_auth_token(user))
            })
        else:
            return Response({
                "User Details": "Invalid Credentials"
            })


class RegisterView(generics.GenericAPIView, mixins.CreateModelMixin):
    """
    TODO:
    Implement register functionality, registering the user by
    taking his details, and returning the Token.
    """
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
        user = self.create(request, validated_data, *args, **kwargs)
        print(user.data['username'])
        user = User.objects.get(username = user.data['username'])
        return Response({'token':str(create_auth_token(user))})


class UserProfileView(generics.GenericAPIView):
    """
    TODO:
    Implement the functionality to retrieve the details
    of the logged in user.
    """
    permission_classes = (permissions.IsAuthenticated, )
    #serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "name": user.first_name,
            "email": user.email,
        })