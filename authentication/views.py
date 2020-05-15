from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.decorators import  api_view
from django.contrib.auth import get_user_model
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
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def  post(self,request):
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'},status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username= username,password = password)
        if user :
           token = create_auth_token(user)
           token = {'token' : token }
           serializer = TokenSerializer(token)
           return Response(serializer.data,status=status.HTTP_200_OK)
        else :
            return Response ({"error" : "Invalid Credentials ! "},status=status.HTTP_400_BAD_REQUEST)    


class RegisterView(generics.GenericAPIView):

    """ 
    TODO:
    Implement register functionality, registering the user by
    taking his details, and returning the Token.
    """
    permission_classes = ()
    serializer_class = RegisterSerializer

    def post(self,request):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
           user =  serializer.create()
           token = create_auth_token(user)
           token = {'token' : token }
           serializer = TokenSerializer(token)
           return Response(serializer.data,status=status.HTTP_201_CREATED)     
        else :
           return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)    
                                                                

class UserProfileView(generics.RetrieveAPIView):
    """
    TODO:
    Implement the functionality to retrieve the details
    of the logged in user.
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get(self,request):

        user = User.objects.get(username= request.user)
        serializer = UserSerializer(user)
        return Response({
            "id" : serializer.data['id'],
            "name" : serializer.data['first_name'],
            "email" : serializer.data['email'],
            "username" : serializer.data['username']
        },status=status.HTTP_200_OK)
        
        
    
