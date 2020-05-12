from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
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
    
    def post(self, request):
        data = request.data
        serializer = self.get_serializer(data)
        answer = serializer.authenticator()
        if (answer is not False):
            token = create_auth_token(answer)
            token = {'token':token}
            serializer=  TokenSerializer(token)
            return Response(serializer.data ,status=status.HTTP_200_OK)
        else:
            now = {
                "non_field_errors": ["Invalid credentials or the user does not exist!"]
            }
            return Response(now ,status = status.HTTP_200_OK)
        pass



class RegisterView(generics.GenericAPIView):
    """
    TODO:
    Implement register functionality, registering the user by
    taking his details, and returning the Token.
    """
    serializer_class = RegisterSerializer

    def post(self, request):
        data = request.data
        serializer = self.get_serializer(data)
        answer = serializer.do()
        token = create_auth_token(answer)
        token = {'token':token}
        serializer=  TokenSerializer(token)
        return Response(serializer.data ,status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveAPIView):
    """
    TODO:
    Implement the functionality to retrieve the details
    of the logged in user.
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserSerializer

    def get(self, request):
        user = User.objects.filter(username = request.user).first()
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
