from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.http import HttpResponse, JsonResponse
from .serializers import (
    LoginSerializer, RegisterSerializer, UserSerializer, TokenSerializer)
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
    serializer_class = LoginSerializer
    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = create_auth_token(user)
        data = {'token': token }
        tokenserializer = TokenSerializer(data)
        return JsonResponse(tokenserializer.data, status=200)


class RegisterView(generics.GenericAPIView):
    """
    TODO:
    Implement register functionality, registering the user by
    taking his details, and returning the Token.
    """
    serializer_class = RegisterSerializer
    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        token = create_auth_token(user)
        data= {'token' : token }
        tokenserializer = TokenSerializer(data)
        return JsonResponse(tokenserializer.data,status=200)

class UserProfileView(generics.RetrieveAPIView):
    """
    TODO:
    Implement the functionality to retrieve the details
    of the logged in user.
    """
    serializer_class = UserSerializer
    def get(self,request):
        userid = request.user.id
        try :
            user = User.objects.get(id=userid)
        except User.DoesNotExist:
            return HttpResponse(status=404)
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data,status=200)
