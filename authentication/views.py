from rest_framework import permissions
from rest_framework import viewsets,generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from .serializers import (
    LoginSerializer, RegisterSerializer, UserSerializer, TokenSerializer)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated


def create_auth_token(user):
    """
    Returns the token required for authentication for a user.
    """
    token, _ = Token.objects.get_or_create(user=user)
    return token
    
class LoginView(generics.GenericAPIView):
    serializer_class=LoginSerializer
    def post(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            user=authenticate(username=serializer.data['username'],password=serializer.data['password'])
            if user is not None:
                queryset={"Token":Token.objects.get(user=user).key}
                return JsonResponse({"Token":Token.objects.get(user=user).key},status=status.HTTP_200_OK)
            else:
                return JsonResponse({"Error":"User credientials donot match"},status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class RegisterView(generics.GenericAPIView):
    serializer_class=RegisterSerializer
    def post(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            user=User.objects.create_user(username=serializer.data['username'],email=serializer.data['email'],password=serializer.data['password'],first_name=serializer.data['first_name'],last_name=serializer.data['last_name'])
            user.save()
            token=create_auth_token(user)
            return JsonResponse({"Token":token.key})
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,) 
    def get(self,request):
        try:
            token=request.headers['Authorization']
            print(token)
            userToken = Token.objects.get(key=token.split()[1])
            userdata=User.objects.get(username=userToken.user)
            serialiser = UserSerializer(userdata)
            return JsonResponse(serialiser.data)
        except KeyError:
             return JsonResponse({"Error":"No auth key found"})