from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
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
    serializer_class=LoginSerializer

    def post(self, request):
        data=request.data
        username=data.get('username')
        password=data.get('password')
        user=authenticate(username=username, password=password)
        if user is not None:
            token = create_auth_token(user)
            Token=TokenSerializer({'token':token})
            return Response(Token.data ,status=status.HTTP_200_OK)
        else:
            error= {
                "errors": ["Invalid input"]
            }
            return Response(error ,status = status.HTTP_200_OK)
        
class RegisterView(generics.CreateAPIView):
    """
    TODO:
    Implement register functionality, registering the user by
    taking his details, and returning the Token.
    """
    serializer_class = RegisterSerializer
    permission_class=[permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            validated_data=serializer.validated_data
        user=self.create(request, validated_data, *args, **kwargs)    
        user=User.objects.get(username=user.data['username'])
        token=create_auth_token(user)
        return Response({'token':token.key} ,status=status.HTTP_200_OK)

class UserProfileView(generics.RetrieveAPIView):
    """
    TODO:
    Implement the functionality to retrieve the details
    of the logged in user.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    queryset=User.objects.all()

    def get_object(self):
        return self.request.user