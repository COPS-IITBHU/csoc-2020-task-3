from rest_framework import permissions
from rest_framework import generics ,mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .serializers import (
    LoginSerializer, RegisterSerializer, UserSerializer, TokenSerializer)
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


def create_auth_token(user):
    """
    Returns the token required for authentication for a user.
    """
    token, _ = Token.objects.get_or_create(user=user)
    return token


class LoginView(generics.GenericAPIView,mixins.ListModelMixin):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = LoginSerializer
    def post(self,request):
        data=request.data
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            token=create_auth_token(user)
            response={
            'token':token.key
            }
            return Response(response)
        else :
            return Response(status=status.HTTP_404_NOT_FOUND)

    


class RegisterView(generics.GenericAPIView,mixins.RetrieveModelMixin,):

    model = get_user_model()
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = RegisterSerializer
    def post(self,request):
        UserModel = get_user_model()
        validated_data=request.data
        print(request.data)
        user = UserModel.objects.create(
            username=validated_data['username'],
            first_name=validated_data['name'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        response={
            'token':token.key
        }

        return Response(response,status=status.HTTP_201_CREATED)


    
    
    
    
    


class UserProfileView(generics.RetrieveAPIView):
    pass


    

