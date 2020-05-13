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
    serializer_class = LoginSerializer
    
    def post(self, request):
        # If user is already authenticated, return 403-Forbidden
        if request.user.is_authenticated:
           return Response(status.HTTP_403_FORBIDDEN)

        # deserialize the data from the POST request
        serializer = self.get_serializer(request.data)
        serializer.run_validation()
        # Run the authenticator function and store its return value
        auth_value = serializer.authenticator()
        # If authentication is successful, auth_value = User
        if (auth_value is not None):
            # Create a token for the user
            token = create_auth_token(auth_value)
            token = {'token':token}
            # Serialise the token
            serializer = TokenSerializer(token)
            # Return the Token with status 200
            return Response(serializer.data ,status=status.HTTP_200_OK)
        
        # If authentication is unsuccessful, auth_value = None
        else:
            # Return with 401 status
            now = {
                "non_field_errors": ["Invalid credentials or the user does not exist!"]
            }
            return Response(now, status = status.HTTP_400_BAD_REQUEST)

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    
    def post(self, request):
        # If user is already authenticated, return 403-Forbidden
        if request.user.is_authenticated:
            return Response(status.HTTP_403_FORBIDDEN)

        # deserialize the request data
        serializer = self.get_serializer(request.data)
        # Register the user
        serializer.run_validation()
        # Register the user
        newUser = serializer.register()
        # Create token
        token = create_auth_token(newUser)
        token = {'token':token}
        # Return token with status 200
        serializer = TokenSerializer(token)
        return Response(serializer.data, status = status.HTTP_200_OK)

class UserProfileView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserSerializer

    def get(self, request):
        # Get the user
        user = User.objects.get(username = request.user)
        # Serialize the data
        serializer = self.get_serializer(user)
        # Return response with status 200 and data
        return Response(serializer.data, status=status.HTTP_200_OK)