from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)


class LoginSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=100)
    password=serializers.CharField(max_length=100)

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('username','password','email','first_name','last_name')
    

class UserSerializer(serializers.ModelSerializer):
    name= serializers.CharField(source='get_full_name')
    class Meta:
        model=User
        fields=['id','name','email','username']