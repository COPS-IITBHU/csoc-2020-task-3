from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import (
    LoginSerializer, RegisterSerializer, UserSerializer, TokenSerializer)
from django.contrib.auth import login,logout,authenticate
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User


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
    serializer_class=LoginSerializer
    def post(self,request):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        login(request,user)
        token=create_auth_token(user)
        return Response({'token':token.key}, status=status.HTTP_200_OK)
        
        


class RegisterView(generics.GenericAPIView):
    """
    TODO:
    Implement register functionality, registering the user by
    taking his details, and returning the Token.
    """
    serializer_class=RegisterSerializer
    def post(self, request):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username=serializer.validated_data['username']
        first_name=serializer.validated_data['first_name']
        last_name=serializer.validated_data['last_name']
        email=serializer.validated_data['email']
        password=serializer.validated_data['password']
        registered_user=User.objects.create_user(username=username,email=email,password=password,first_name=first_name, last_name=last_name)
        registered_user.save()
        user=authenticate(request=None,username=username,password=password)
        login(request,user)
        token=create_auth_token(user)
        return Response({'token':token.key}, status=status.HTTP_200_OK)



class UserProfileView(generics.RetrieveAPIView):
    """
    TODO:
    Implement the functionality to retrieve the details
    of the logged in user.
    """
    permission_classes = (permissions.IsAuthenticated, )
    def get(self, request):
        userlog=UserSerializer(request.user)
        return Response(userlog.data)
    