from django.http import JsonResponse
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status,mixins
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate,login
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
    queryset= User.objects.all()
    serializer_class=LoginSerializer

    def post(self, request):
        data = request.data

        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            token=create_auth_token(user)
            tokenserializer=TokenSerializer({'token':token})
            return Response(tokenserializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class RegisterView(generics.GenericAPIView,mixins.CreateModelMixin):
    """
    TODO:
    Implement register functionality, registering the user by
    taking his details, and returning the Token.
    """
    queryset= User.objects.all()
    serializer_class=RegisterSerializer

    def post(self,request): 
        serializer = self.get_serializer(data=request.data)  
        self.create(request)
        username=request.data['username']
        user=User.objects.get(username=username)  
        token=create_auth_token(user)
        tokenserializer=TokenSerializer({'token':token})
        return Response(tokenserializer.data)
        
       


class UserProfileView(generics.RetrieveAPIView):
    """
    TODO:
    Implement the functionality to retrieve the details
    of the logged in user.
    """
    permission_classes = (permissions.IsAuthenticated, )
    queryset= User.objects.all()
    serializer_class=UserSerializer

    def get_object(self):
        return self.request.user