from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User

from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
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
    serializer_class = LoginSerializer
    

    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user_name = request.data['username']
            password = request.data['password']
            user = authenticate(username=user_name,password=password)
            if user:
                # login(request,user)
                response = {"token":str(create_auth_token(user))}
                
                return Response(response,status=status.HTTP_200_OK)
            
            response = {
                "Error":"Invalid Credentials"
            }
            return Response(response,status=status.HTTP_401_UNAUTHORIZED)
        # else:
        #     response = {
        #         "Error":"Please enter valid data"
        #     }
        #     return Response(response,status=status.HTTP_400_BAD_REQUEST)

    


class RegisterView(generics.GenericAPIView):
    """
    TODO:
    Implement register functionality, registering the user by
    taking his details, and returning the Token.
    """
    serializer_class = RegisterSerializer
    

    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # user_name = request.data['username']
            # password = request.data['password']
            # user = authenticate(username=user_name,password=password)
            user = User.objects.get(username = request.data['username'])
            # login(request,user)
            response = {"token":str(create_auth_token(user))}
                
            return Response(response,status=status.HTTP_200_OK)
        else:
            response = {
                "Error":"Please enter valid data"
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveAPIView):
    """
    TODO:
    Implement the functionality to retrieve the details
    of the logged in user.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer
    def get(self,request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    